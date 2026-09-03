"""V-Droid verifier 驱动的 AppSim Agent。"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Optional

from PIL import Image

from ..base import AgentExecutionResult, BaseAgent
from ..m3a_agent.action_executor import ActionExecutor
from ..m3a_agent.m3a_utils import parse_reason_action_output
from ..m3a_agent.u2_env import U2Env, UIElement
from .action_space import (
    build_candidate_actions,
    build_rule_summary,
    describe_ui_elements,
    needs_completion,
    parse_action,
)
from .clients import HelperLLMClient, VDroidInfrastructureError, VerifierClient
from .official import OfficialComponents, load_official_components

logger = logging.getLogger(__name__)


class VDroidActionCompletionError(RuntimeError):
    """helper 在当前 step 内重试耗尽。"""


def _extract_json_action(response_text: str) -> dict[str, Any]:
    _, action_text = parse_reason_action_output(response_text)
    if action_text:
        return parse_action(action_text)

    decoder = json.JSONDecoder()
    for index, character in enumerate(response_text):
        if character != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(response_text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict) and parsed.get("action_type"):
            return parsed
    raise ValueError(f"辅助 LLM 未返回有效动作 JSON: {response_text}")


class VDroidAgent(BaseAgent):
    """使用本地 verifier 排序离散动作，并通过 uiautomator2 执行。"""

    def __init__(
        self,
        verifier_api_base: str,
        helper_api_key: str,
        helper_api_base: str,
        helper_model_name: str,
        device_id: str,
        official_code_dir: str,
        screenshots_dir: str = "screenshots",
        max_steps: int = 50,
        max_action_completion_attempts: int = 3,
        wait_after_action_seconds: float = 2.0,
        verifier_timeout_seconds: float = 300.0,
        helper_timeout_seconds: float = 300.0,
        helper_max_tokens: int = 512,
        verifier_batch_size: int = 64,
        summary_mode: str = "llm",
        history_turns: int = 20,
        allow_app_switch: bool = False,
        stagnation_limit: int = 50,
        review_terminal_actions: bool = True,
        device_connect_attempts: int = 3,
        device_connect_retry_seconds: float = 2.0,
    ):
        if max_steps <= 0:
            raise ValueError("VDROID_MAX_STEPS 必须大于 0")
        if max_action_completion_attempts <= 0:
            raise ValueError("VDROID_ACTION_COMPLETION_ATTEMPTS 必须大于 0")
        if wait_after_action_seconds < 0:
            raise ValueError("VDROID_WAIT_AFTER_ACTION_SECONDS 不能小于 0")
        if summary_mode not in {"llm", "rule"}:
            raise ValueError("VDROID_SUMMARY_MODE 必须为 llm 或 rule")
        if history_turns <= 0 or stagnation_limit <= 0:
            raise ValueError("VDROID_HISTORY_TURNS 和 VDROID_STAGNATION_LIMIT 必须大于 0")
        if device_connect_attempts <= 0 or device_connect_retry_seconds < 0:
            raise ValueError(
                "VDROID_DEVICE_CONNECT_ATTEMPTS 必须大于 0，重试间隔不能小于 0"
            )

        self.device_id = device_id
        self.screenshots_dir = screenshots_dir
        self.max_steps = max_steps
        self.max_action_completion_attempts = max_action_completion_attempts
        self.wait_after_action_seconds = wait_after_action_seconds
        self.summary_mode = summary_mode
        self.history_turns = history_turns
        self.allow_app_switch = allow_app_switch
        self.stagnation_limit = stagnation_limit
        self.review_terminal_actions = review_terminal_actions
        self.current_task_folder: Optional[str] = None
        self.history: list[str] = []

        self.official: OfficialComponents = load_official_components(official_code_dir)
        self.verifier = VerifierClient(
            verifier_api_base,
            timeout_seconds=verifier_timeout_seconds,
            max_batch_size=verifier_batch_size,
        )
        health = self.verifier.check_health()
        logger.info(
            "V-Droid verifier 已就绪: endpoint=%s gpu=%s",
            self.verifier.base_url,
            health.get("cuda_visible_devices", ""),
        )
        self.helper_llm = HelperLLMClient(
            api_key=helper_api_key,
            api_base=helper_api_base,
            model_name=helper_model_name,
            timeout_seconds=helper_timeout_seconds,
            max_tokens=helper_max_tokens,
        )

        os.makedirs(self.screenshots_dir, exist_ok=True)
        self.env = U2Env(
            device_id,
            connect_attempts=device_connect_attempts,
            connect_retry_seconds=device_connect_retry_seconds,
        )
        self.action_executor = ActionExecutor(self.env.u2_device)
        self.target_package = None

    def reset(self) -> None:
        """清空当前任务历史。"""

        self.history = []

    def close(self) -> None:
        """关闭 HTTP 客户端并释放设备引用。"""

        self.helper_llm.close()
        self.env.close()

    def _save_screenshot(self, pixels: Any, step: int) -> Optional[str]:
        try:
            save_dir = self.current_task_folder or self.screenshots_dir
            os.makedirs(save_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            path = os.path.join(save_dir, f"screenshot_step_{step}_{timestamp}.png")
            Image.fromarray(pixels).save(path)
            return path
        except Exception as error:
            logger.error("保存 V-Droid 截图失败: %s", error)
            return None

    def _history_for_prompt(self, history: list[str]) -> list[str]:
        history_turns = getattr(self, "history_turns", 20)
        selected_history = history[-history_turns:]
        start_index = len(history) - len(selected_history)
        return [
            f"Step {start_index + index + 1}- {summary}"
            for index, summary in enumerate(selected_history)
        ]

    @staticmethod
    def _ui_fingerprint(package_name: str, ui_description: str) -> str:
        payload = f"{package_name}\n{ui_description}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @staticmethod
    def _action_target(
        action: dict[str, Any],
        ui_elements: list[UIElement],
    ) -> Optional[dict[str, Any]]:
        index = action.get("index")
        if not isinstance(index, int) or not 0 <= index < len(ui_elements):
            return None
        element = ui_elements[index]
        return {
            "index": index,
            "bounds": list(element.bounds),
            "text": element.text,
            "content_description": element.content_description,
            "hint_text": element.hint_text,
            "resource_name": element.resource_name,
            "class_name": element.class_name,
            "package_name": element.package_name,
        }

    def _restore_target_package(self) -> bool:
        target_package = getattr(self, "target_package", None)
        if not target_package:
            return False
        current_package = self.env.current_package()
        if not current_package or current_package == target_package:
            return False
        logger.warning(
            "V-Droid 检测到离开目标 App，自动恢复: current=%s target=%s",
            current_package,
            target_package,
        )
        self.env.u2_device.app_start(target_package)
        time.sleep(1)
        restored_package = self.env.current_package()
        if restored_package != target_package:
            raise VDroidInfrastructureError(
                "无法恢复目标 App: "
                f"expected={target_package} actual={restored_package}"
            )
        return True

    @staticmethod
    def _validate_action(action: dict[str, Any], ui_elements: list[UIElement]) -> None:
        action_type = action.get("action_type")
        index = action.get("index")
        allowed_action_types = {
            "answer",
            "clear_text",
            "click",
            "input_text",
            "long_press",
            "navigate_back",
            "navigate_home",
            "open_app",
            "scroll",
            "status",
            "wait",
        }
        if action_type not in allowed_action_types:
            raise ValueError(f"不支持的动作类型: {action}")
        if action_type in {"click", "long_press", "input_text", "clear_text"}:
            if not isinstance(index, int) or not 0 <= index < len(ui_elements):
                raise ValueError(f"动作 index 无效: {action}")
        if action_type == "scroll" and index is not None:
            if not isinstance(index, int) or not 0 <= index < len(ui_elements):
                raise ValueError(f"scroll index 无效: {action}")
        if action_type == "scroll" and action.get("direction") not in {
            "up",
            "down",
            "left",
            "right",
        }:
            raise ValueError(f"scroll direction 无效: {action}")
        required_fields = {
            "input_text": "text",
            "open_app": "app_name",
            "answer": "text",
        }
        field = required_fields.get(str(action_type))
        if field and not str(action.get(field, "")).strip():
            raise ValueError(f"动作缺少 {field}: {action}")
        if needs_completion(action):
            raise ValueError(f"动作仍包含占位符: {action}")

    def _complete_action(
        self,
        goal: str,
        original_action: dict[str, Any],
        ui_description: str,
        attempts: int,
        prompt_suffix: str = "",
    ) -> tuple[dict[str, Any], str]:
        original_text = json.dumps(
            original_action,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        prompt = self.official.action_completion_prompt(
            goal,
            original_text,
            self._history_for_prompt(self.history),
            ui_description,
        )
        if prompt_suffix:
            prompt = f"{prompt}\n{prompt_suffix}"
        last_error: Optional[Exception] = None
        for attempt in range(1, attempts + 1):
            logger.info(
                "调用 V-Droid 第三方 helper LLM: protocol=%s model=%s "
                "action_type=%s attempt=%s/%s",
                self.helper_llm.api_mode,
                self.helper_llm.model_name,
                original_action.get("action_type"),
                attempt,
                attempts,
            )
            logger.info(
                "发送给 V-Droid 第三方 helper LLM 的提示词预览（最多 10 字）: %s",
                prompt.replace("\r", " ").replace("\n", " ")[:10],
            )
            try:
                response_text, _ = self.helper_llm.complete_action(prompt)
            except VDroidInfrastructureError as error:
                last_error = error
                if attempt >= attempts:
                    raise VDroidActionCompletionError(
                        f"V-Droid helper LLM 连续失败 {attempts} 次"
                    ) from error
                retry_delay = 2**attempt
                logger.warning(
                    "V-Droid helper LLM 调用失败，%s 秒后重试 %s/%s: %s",
                    retry_delay,
                    attempt,
                    attempts,
                    error,
                )
                time.sleep(retry_delay)
                continue
            logger.info(
                "V-Droid 第三方 helper LLM 输出预览（最多 10 字）: %s",
                response_text.replace("\r", " ").replace("\n", " ")[:10],
            )
            try:
                completed = _extract_json_action(response_text)
                if completed != original_action:
                    logger.info(
                        "V-Droid helper 覆盖 verifier 候选动作: %s -> %s",
                        original_action,
                        completed,
                    )
                return completed, response_text
            except (json.JSONDecodeError, ValueError) as error:
                last_error = error
                logger.warning(
                    "V-Droid 动作补全格式错误，重试 %s/%s: %s",
                    attempt,
                    attempts,
                    error,
                )
        raise ValueError(f"V-Droid 动作补全失败: {last_error}")

    def _select_action(
        self,
        goal: str,
        ui_elements: list[UIElement],
        completion_attempts: int,
        excluded_candidates: Optional[set[str]] = None,
    ) -> tuple[
        dict[str, Any],
        float,
        list[dict[str, Any]],
        Optional[str],
        dict[str, Any],
    ]:
        ui_description = describe_ui_elements(ui_elements)
        candidates = build_candidate_actions(
            ui_elements,
            include_app_switch=getattr(self, "allow_app_switch", False),
        )
        prompt_history = self._history_for_prompt(self.history)
        prompts = [
            self.official.action_selection_prompt(
                action,
                prompt_history,
                goal,
                ui_description,
            )
            for action in candidates
        ]
        scores = self.verifier.score(prompts)
        ranked = sorted(
            zip(candidates, scores, strict=True),
            key=lambda item: item[1],
            reverse=True,
        )
        ranking = [
            {"action": parse_action(action), "score": score}
            for action, score in ranked[:10]
        ]

        completion_errors: list[str] = []
        for action_text, score in ranked:
            if excluded_candidates and action_text in excluded_candidates:
                logger.info("V-Droid 跳过当前 UI 已确认无效的候选动作: %s", action_text)
                continue
            action = parse_action(action_text)
            selected_candidate = dict(action)
            helper_response = None
            prompt_suffix = ""
            requires_helper = needs_completion(action)
            if (
                action.get("action_type") == "status"
                and getattr(self, "review_terminal_actions", True)
            ):
                requires_helper = True
                prompt_suffix = (
                    "The selected status action may be premature. Verify whether the "
                    "goal is actually complete from the current UI and history. If it is "
                    "complete, return the same status action. Otherwise, replace it with "
                    "one executable next action for the current UI. Return only Action: "
                    "followed by one JSON object."
                )
            if requires_helper:
                try:
                    action, helper_response = self._complete_action(
                        goal,
                        action,
                        ui_description,
                        completion_attempts,
                        prompt_suffix=prompt_suffix,
                    )
                except ValueError as error:
                    completion_errors.append(str(error))
                    continue
            if (
                not getattr(self, "allow_app_switch", False)
                and action.get("action_type") in {"navigate_home", "open_app"}
            ):
                completion_errors.append(f"AppSim 禁止跨 App 动作: {action}")
                continue
            try:
                self._validate_action(action, ui_elements)
            except ValueError as error:
                completion_errors.append(str(error))
                continue
            return action, score, ranking, helper_response, selected_candidate
        raise ValueError(
            "V-Droid 没有可执行候选动作: " + "; ".join(completion_errors[-3:])
        )

    def _clear_text(self, action: dict[str, Any], ui_elements: list[UIElement]) -> bool:
        index = action["index"]
        left, top, right, bottom = ui_elements[index].bounds
        self.env.u2_device.click((left + right) // 2, (top + bottom) // 2)
        if hasattr(self.env.u2_device, "clear_text"):
            self.env.u2_device.clear_text()
        else:
            self.env.u2_device.send_keys("", clear=True)
        return True

    def _execute_action(
        self,
        action: dict[str, Any],
        ui_elements: list[UIElement],
    ) -> tuple[bool, bool, Optional[str]]:
        action_type = action["action_type"]
        if action_type == "status":
            complete = action.get("goal_status") == "complete"
            message = "任务已完成" if complete else "任务不可行"
            return True, complete, message
        if action_type == "answer":
            return True, True, str(action.get("text", ""))
        if action_type == "clear_text":
            return False, self._clear_text(action, ui_elements), None
        return False, self.action_executor.execute_action(action, ui_elements), None

    def _summarize_action(
        self,
        goal: str,
        action: dict[str, Any],
        before_ui_elements: list[UIElement],
        after_ui_elements: list[UIElement],
        executed: bool,
    ) -> str:
        rule_summary = build_rule_summary(action, before_ui_elements)
        if not executed:
            return f"Action execution failed. {rule_summary}"
        if getattr(self, "summary_mode", "llm") != "llm":
            return rule_summary

        action_text = json.dumps(action, ensure_ascii=False, separators=(",", ":"))
        prompt = self.official.summarize_prompt(
            action_text,
            "",
            goal,
            describe_ui_elements(before_ui_elements),
            describe_ui_elements(after_ui_elements),
        )
        logger.info(
            "调用 V-Droid 第三方 helper LLM: protocol=%s model=%s purpose=summary",
            self.helper_llm.api_mode,
            self.helper_llm.model_name,
        )
        logger.info(
            "发送给 V-Droid 第三方 helper LLM 的提示词预览（最多 10 字）: %s",
            prompt.replace("\r", " ").replace("\n", " ")[:10],
        )
        try:
            response_text, _ = self.helper_llm.complete_action(prompt)
        except VDroidInfrastructureError as error:
            logger.warning("V-Droid 工作记忆生成失败，降级为规则摘要: %s", error)
            return rule_summary
        logger.info(
            "V-Droid 第三方 helper LLM 输出预览（最多 10 字）: %s",
            response_text.replace("\r", " ").replace("\n", " ")[:10],
        )
        summary = " ".join(response_text.split()).strip()
        if not summary:
            return rule_summary
        return f"Action selected: {action_text}. {summary[:500]}"

    def execute_instruction(
        self,
        instruction: str,
        max_steps: Optional[int] = None,
        max_attempts_per_step: Optional[int] = None,
    ) -> AgentExecutionResult:
        """执行一个 AppSim 任务。"""

        step_limit = max_steps if max_steps is not None else self.max_steps
        completion_attempts = (
            max_attempts_per_step
            if max_attempts_per_step is not None
            else self.max_action_completion_attempts
        )
        if step_limit <= 0 or completion_attempts <= 0:
            raise ValueError("max_steps 和 max_attempts_per_step 必须大于 0")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_instruction = instruction.replace("/", "_").replace("\\", "_").strip()[:50]
        self.current_task_folder = os.path.join(
            self.screenshots_dir,
            f"{timestamp}_{safe_instruction}",
        )
        os.makedirs(self.current_task_folder, exist_ok=True)
        self.history = []

        executed_actions: list[dict[str, Any]] = []
        screenshots: list[str] = []
        final_message: Optional[str] = None
        task_success = False
        error_message: Optional[str] = None
        cached_state: Optional[dict[str, Any]] = None
        candidate_attempts_by_state: dict[tuple[str, str], int] = {}
        stagnation_limit = getattr(self, "stagnation_limit", 2)

        try:
            for step in range(1, step_limit + 1):
                logger.info("V-Droid step %s/%s: %s", step, step_limit, instruction)
                if self._restore_target_package():
                    cached_state = None
                state = cached_state or self.env.get_state(wait_to_stabilize=True)
                cached_state = None
                ui_elements = state["ui_elements"]
                ui_description = describe_ui_elements(ui_elements)
                current_package = self.env.current_package() or ""
                ui_state_key = self._ui_fingerprint(current_package, ui_description)
                excluded_candidates = {
                    candidate
                    for (state_key, candidate), count in candidate_attempts_by_state.items()
                    if state_key == ui_state_key and count >= stagnation_limit
                }
                screenshot_path = self._save_screenshot(state["pixels"], step)
                if screenshot_path:
                    screenshots.append(screenshot_path)

                action, score, ranking, helper_response, selected_candidate = self._select_action(
                    instruction,
                    ui_elements,
                    completion_attempts,
                    excluded_candidates=excluded_candidates,
                )
                candidate_text = json.dumps(
                    selected_candidate,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                candidate_key = (ui_state_key, candidate_text)
                candidate_attempts_by_state[candidate_key] = (
                    candidate_attempts_by_state.get(candidate_key, 0) + 1
                )
                action_target = self._action_target(action, ui_elements)
                done, executed, action_message = self._execute_action(action, ui_elements)
                if done:
                    summary = build_rule_summary(action, ui_elements)
                else:
                    if self.wait_after_action_seconds:
                        time.sleep(self.wait_after_action_seconds)
                    if self._restore_target_package():
                        executed = False
                    after_state = self.env.get_state(wait_to_stabilize=True)
                    after_ui_elements = after_state["ui_elements"]
                    summary = self._summarize_action(
                        instruction,
                        action,
                        ui_elements,
                        after_ui_elements,
                        executed,
                    )
                    if not executed:
                        candidate_attempts_by_state[candidate_key] = stagnation_limit
                    cached_state = after_state
                self.history.append(summary)
                executed_actions.append(
                    {
                        "step": step,
                        "done": done,
                        "summary": summary,
                        "action_json": action,
                        "action_target": action_target,
                        "selected_candidate": selected_candidate,
                        "helper_overrode_candidate": action != selected_candidate,
                        "verifier_score": score,
                        "top_candidates": ranking,
                        "helper_response": helper_response,
                        "screenshot": screenshot_path,
                    }
                )

                if done:
                    task_success = executed
                    final_message = action_message or summary
                    break
            else:
                error_message = f"达到最大步数限制 ({step_limit})，任务未完成"

            return AgentExecutionResult(
                success=task_success,
                completed_steps=len(executed_actions),
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshot_dir=self.current_task_folder,
                screenshots=screenshots,
                error=error_message,
                final_message=final_message,
            )
        except VDroidInfrastructureError:
            raise
        except Exception as error:
            logger.exception("V-Droid 执行失败")
            return AgentExecutionResult(
                success=False,
                completed_steps=len(executed_actions),
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshot_dir=self.current_task_folder,
                screenshots=screenshots,
                error=f"V-Droid 执行失败: {error}",
                final_message=None,
            )
        finally:
            self.current_task_folder = None
