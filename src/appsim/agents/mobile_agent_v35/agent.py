# -*- coding: utf-8 -*-
"""在 AppSim 中运行官方 Mobile-Agent-v3.5。"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..base import AgentExecutionResult, BaseAgent
from .client_adapter import configure_official_wrapper_client
from .env_adapter import MobileAgentAppSimEnvAdapter
from .official import OfficialBindings, load_official_bindings

logger = logging.getLogger(__name__)


class MobileAgentV35Agent(BaseAgent):
    """用 AppSim 生命周期包装官方 Mobile-Agent-v3.5。"""

    def __init__(
        self,
        api_key: str,
        api_base: str,
        model_name: str,
        device_id: str,
        app_package: str,
        official_code_dir: str,
        screenshots_dir: str = "screenshots",
        max_steps: int = 50,
        max_tokens: int = 512,
        request_timeout_seconds: float = 300.0,
        wait_after_action_seconds: float = 3.0,
        official_bindings: Optional[OfficialBindings] = None,
        environment: Optional[MobileAgentAppSimEnvAdapter] = None,
    ) -> None:
        if not api_base:
            raise ValueError("MobileAgent-v3.5 requires MOBILE_AGENT_V35_API_BASE or API_BASE")
        if not device_id:
            raise ValueError("MobileAgent-v3.5 requires device_id")
        if not app_package:
            raise ValueError("MobileAgent-v3.5 requires app_package")
        if max_steps <= 0:
            raise ValueError("MOBILE_AGENT_V35_MAX_STEPS 必须为正整数")
        if max_tokens <= 0:
            raise ValueError("MOBILE_AGENT_V35_MAX_TOKENS 必须为正整数")
        if request_timeout_seconds <= 0:
            raise ValueError("MOBILE_AGENT_V35_REQUEST_TIMEOUT_SECONDS 必须大于 0")
        if wait_after_action_seconds < 0:
            raise ValueError("MOBILE_AGENT_V35_WAIT_AFTER_ACTION_SECONDS 不能小于 0")

        self.api_key = api_key or "EMPTY"
        self.api_base = api_base
        self.model_name = model_name or "GUI-Owl-1.5-8B-Instruct"
        self.device_id = device_id
        self.app_package = app_package
        self.screenshots_dir = screenshots_dir
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.request_timeout_seconds = request_timeout_seconds
        self.wait_after_action_seconds = wait_after_action_seconds

        self.official = official_bindings or load_official_bindings(official_code_dir)
        self.environment = environment or MobileAgentAppSimEnvAdapter(
            device_id=device_id,
            app_package=app_package,
            action_module=self.official.new_json_action,
        )
        # 与官方 run_ma35.py 一致，所有角色共用同一个 GUI-Owl 客户端。
        self.model_wrapper = self.official.GUIOwlWrapper(
            self.api_key,
            self.api_base,
            self.model_name,
        )
        configure_official_wrapper_client(
            self.model_wrapper,
            api_key=self.api_key,
            api_base=self.api_base,
            max_tokens=self.max_tokens,
            timeout_seconds=self.request_timeout_seconds,
        )
        self.current_official_agent: Optional[Any] = None
        self.current_task_folder: Optional[str] = None
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def reset(self) -> None:
        """清理当前 episode；App 数据仍由 AppSim 主流程重置。"""

        self.current_official_agent = None
        self.current_task_folder = None
        self.environment.reset(go_home=False)

    def close(self) -> None:
        """关闭环境和官方模型客户端。"""

        self.environment.close()
        client = getattr(self.model_wrapper, "bot", None)
        if client is not None and hasattr(client, "close"):
            client.close()
        self.current_official_agent = None

    @staticmethod
    def _safe_task_name(instruction: str) -> str:
        return instruction.replace("/", "_").replace("\\", "_").strip()[:50]

    @staticmethod
    def _official_instruction_dir(output_root: Path, instruction: str) -> Path:
        # 官方 step 使用这一规则保存轨迹；这里只预建目录，不改变官方内容。
        return output_root / instruction.replace(" ", "_")[:50]

    @staticmethod
    def _final_message(data: Dict[str, Any], interaction_cache: str) -> Optional[str]:
        if interaction_cache:
            return interaction_cache

        action_history = data.get("action_history") or []
        if action_history and isinstance(action_history[-1], dict):
            last_action = action_history[-1]
            if last_action.get("action") == "answer":
                text = last_action.get("text")
                if text is not None:
                    return str(text)

        finish_thought = data.get("finish_thought")
        return str(finish_thought) if finish_thought else None

    @staticmethod
    def _step_record(step: int, data: Dict[str, Any]) -> Dict[str, Any]:
        action_history = data.get("action_history") or []
        summary_history = data.get("summary_history") or []
        action_outcomes = data.get("action_outcomes") or []
        error_descriptions = data.get("error_descriptions") or []
        return {
            "step": step,
            "action": action_history[-1] if action_history else None,
            "summary": summary_history[-1] if summary_history else None,
            "outcome": action_outcomes[-1] if action_outcomes else None,
            "error_description": (error_descriptions[-1] if error_descriptions else None),
            "plan": data.get("plan"),
            "completed_plan": data.get("completed_plan"),
        }

    @staticmethod
    def _collect_screenshots(task_dir: Path) -> List[str]:
        return [str(path) for path in sorted(task_dir.rglob("screenshot_*.png")) if path.is_file()]

    def execute_instruction(
        self,
        instruction: str,
        max_steps: Optional[int] = None,
    ) -> AgentExecutionResult:
        """循环调用官方 step，直到官方结束或达到 AppSim 步数上限。"""

        step_limit = self.max_steps if max_steps is None else max_steps
        if step_limit <= 0:
            raise ValueError("max_steps 必须为正整数")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_root = Path(self.screenshots_dir) / (f"{timestamp}_{self._safe_task_name(instruction)}")
        output_root.mkdir(parents=True, exist_ok=False)
        official_task_dir = self._official_instruction_dir(
            output_root,
            instruction,
        )
        official_task_dir.mkdir(parents=True, exist_ok=True)
        self.current_task_folder = str(official_task_dir)

        executed_actions: List[Dict[str, Any]] = []
        last_data: Dict[str, Any] = {}
        done = False
        error: Optional[str] = None

        try:
            official_agent = self.official.MobileAgentV3_M3A(
                self.environment,
                self.model_wrapper,
                name="MobileAgent-v3.5",
                wait_after_action_seconds=self.wait_after_action_seconds,
                output_path=str(output_root),
            )
            # 官方 run_ma35.py 使用自动等待模式。
            official_agent.transition_pause = None
            official_agent.reset(go_home_on_reset=False)
            self.current_official_agent = official_agent

            for step in range(1, step_limit + 1):
                interaction_result = official_agent.step(instruction)
                last_data = interaction_result.data or {}
                executed_actions.append(self._step_record(step, last_data))
                if interaction_result.done:
                    done = True
                    break

            if not done:
                error = f"达到最大步数限制 ({step_limit})，任务未完成"
        except Exception as unexpected_error:
            error = f"MobileAgent-v3.5 执行失败: {unexpected_error}"
            logger.exception(error)

        screenshots = self._collect_screenshots(official_task_dir)
        final_message = self._final_message(
            last_data,
            self.environment.interaction_cache,
        )
        action_history = last_data.get("action_history") or []

        return AgentExecutionResult(
            # 官方 done 仅控制停止；真实成功仍由 AppSim verifier 判定。
            success=done,
            completed_steps=len(executed_actions),
            total_actions=len(action_history),
            executed_actions=executed_actions,
            screenshot_dir=str(official_task_dir),
            screenshots=screenshots,
            error=None if done else error,
            final_message=final_message,
        )
