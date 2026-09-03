# -*- coding: utf-8 -*-
"""OpenSource-UI-TRAS 在 AppSim 中的独立 Agent 实现。"""

import base64
import io
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import uiautomator2 as u2
from openai import OpenAI
from PIL import Image

from ..base import AgentExecutionResult, BaseAgent
from .android_executor import AndroidActionExecutor
from .official import OfficialComponents, load_official_components

logger = logging.getLogger(__name__)


class OpenSourceUITRASInfrastructureError(RuntimeError):
    """需要由 AppSim runner 重试的基础设施异常。"""


def _is_context_length_error(error: Exception) -> bool:
    message = str(error).lower()
    return "maximum context length" in message or "context length" in message or "max_model_len" in message


def _response_to_dict(response: Any) -> Optional[Dict[str, Any]]:
    if response is None:
        return None
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if isinstance(response, dict):
        return response
    return {"repr": repr(response)}


class OpenSourceUITRASAgent(BaseAgent):
    """调用本地 OpenAI 兼容接口并控制 Android 设备。"""

    def __init__(
        self,
        api_key: str,
        api_base: str,
        model_name: str,
        device_id: str,
        official_code_dir: str,
        screenshots_dir: str = "screenshots",
        wait_after_action_seconds: float = 2.0,
        max_tokens: int = 400,
        history_turns: int = 8,
        thought_language: str = "English",
        request_timeout_seconds: float = 300.0,
        model_kwargs: Optional[dict] = None,
    ):
        if not api_base:
            raise ValueError("OpenSource-UI-TRAS requires OPEN_SOURCE_UI_TRAS_API_BASE or API_BASE")
        if max_tokens <= 0:
            raise ValueError("OPEN_SOURCE_UI_TRAS_MAX_TOKENS 必须为正整数")
        if history_turns < 0:
            raise ValueError("OPEN_SOURCE_UI_TRAS_HISTORY_TURNS 不能小于 0")
        if not thought_language.strip():
            raise ValueError("OPEN_SOURCE_UI_TRAS_THOUGHT_LANGUAGE 不能为空")
        if request_timeout_seconds <= 0:
            raise ValueError("OPEN_SOURCE_UI_TRAS_REQUEST_TIMEOUT_SECONDS 必须大于 0")

        self.api_key = api_key or "EMPTY"
        self.api_base = api_base
        self.model_name = model_name or "OpenSource-UI-TRAS"
        self.device_id = device_id
        self.screenshots_dir = screenshots_dir
        self.wait_after_action_seconds = wait_after_action_seconds
        self.max_tokens = max_tokens
        self.history_turns = history_turns
        self.thought_language = thought_language
        self.request_timeout_seconds = request_timeout_seconds
        self.model_kwargs = model_kwargs or {}
        self.official: OfficialComponents = load_official_components(official_code_dir)

        os.makedirs(self.screenshots_dir, exist_ok=True)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base,
            timeout=self.request_timeout_seconds,
            max_retries=0,
        )
        self.u2_device = u2.connect(self.device_id)
        self.action_executor = AndroidActionExecutor(self.u2_device)
        self.history: List[Dict[str, str]] = []
        self.current_task_folder: Optional[str] = None

        info = self.u2_device.info
        logger.info("OpenSource-UI-TRAS uiautomator2 连接成功: %s", self.device_id)
        logger.info(
            "屏幕尺寸: %sx%s",
            info.get("displayWidth", "Unknown"),
            info.get("displayHeight", "Unknown"),
        )

    def reset(self) -> None:
        """清空当前任务的模型历史。"""

        self.history = []

    def close(self) -> None:
        """关闭 API 客户端并释放设备引用。"""

        if self.client:
            self.client.close()
        self.u2_device = None

    def _get_screenshot(self) -> Image.Image:
        screenshot = self.u2_device.screenshot()
        if isinstance(screenshot, Image.Image):
            return screenshot.convert("RGB")
        return Image.fromarray(screenshot).convert("RGB")

    def _save_screenshot(self, image: Image.Image, step: int) -> Optional[str]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"screenshot_step_{step}_{timestamp}.png"
            save_dir = self.current_task_folder or self.screenshots_dir
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)
            return save_path
        except Exception as error:
            logger.error("保存截图失败: %s", error)
            return None

    @staticmethod
    def _encode_image(image: Image.Image) -> str:
        with io.BytesIO() as image_buffer:
            image.save(image_buffer, format="JPEG", quality=90)
            return base64.b64encode(image_buffer.getvalue()).decode("utf-8")

    @staticmethod
    def _image_content(image_b64: str) -> Dict[str, Any]:
        return {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
        }

    def _build_prompt(self, instruction: str) -> str:
        return self.official.mobile_prompt.format(
            language=self.thought_language,
            instruction=instruction,
        )

    def _build_messages(
        self,
        instruction: str,
        current_image_b64: str,
        include_history: bool = True,
    ) -> List[Dict[str, Any]]:
        history = self.history[-self.history_turns :] if include_history and self.history_turns else []
        prompt = self._build_prompt(instruction)
        messages: List[Dict[str, Any]] = []

        for index, turn in enumerate(history):
            user_content: List[Dict[str, Any]] = []
            if index == 0:
                user_content.append({"type": "text", "text": prompt})
            user_content.append(self._image_content(turn["image_b64"]))
            messages.append({"role": "user", "content": user_content})
            messages.append(
                {
                    "role": "assistant",
                    "content": self.official.add_box_token(turn["assistant_content"]),
                }
            )

        current_content: List[Dict[str, Any]] = []
        if not history:
            current_content.append({"type": "text", "text": prompt})
        current_content.append(self._image_content(current_image_b64))
        messages.append({"role": "user", "content": current_content})
        return messages

    @staticmethod
    def _extract_response_text(response: Any) -> str:
        content = response.choices[0].message.content
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            text_parts: List[str] = []
            for part in content:
                if isinstance(part, dict) and part.get("text"):
                    text_parts.append(str(part["text"]))
                elif getattr(part, "text", None):
                    text_parts.append(str(part.text))
            return "\n".join(text_parts).strip()
        return ""

    def _call_llm(
        self,
        instruction: str,
        image_b64: str,
    ) -> Tuple[str, bool, Any]:
        messages = self._build_messages(
            instruction,
            image_b64,
            include_history=True,
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.0,
                max_tokens=self.max_tokens,
                **self.model_kwargs,
            )
            return self._extract_response_text(response), False, response
        except Exception as error:
            if not _is_context_length_error(error) or not self.history:
                raise
            logger.warning("OpenSource-UI-TRAS 上下文过长，降级为仅发送当前截图")
            # 立即丢弃已超长历史，避免外层重试再次发送同一批内容。
            self.history = []

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self._build_messages(
                instruction,
                image_b64,
                include_history=False,
            ),
            temperature=0.0,
            max_tokens=self.max_tokens,
            **self.model_kwargs,
        )
        response_text = self._extract_response_text(response)
        return response_text, True, response

    def execute_instruction(
        self,
        instruction: str,
        max_steps: int = 50,
        max_attempts_per_step: int = 3,
    ) -> AgentExecutionResult:
        if max_steps <= 0:
            raise ValueError("max_steps 必须为正整数")
        if max_attempts_per_step <= 0:
            raise ValueError("max_attempts_per_step 必须为正整数")

        logger.info("开始执行 OpenSource-UI-TRAS 任务: %s", instruction)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_instruction = instruction.replace("/", "_").replace("\\", "_").strip()[:50]
        task_folder = os.path.join(
            self.screenshots_dir,
            f"{timestamp}_{safe_instruction}",
        )
        self.current_task_folder = task_folder
        os.makedirs(task_folder, exist_ok=True)

        self.history = []
        executed_actions: List[Dict[str, Any]] = []
        screenshots: List[str] = []
        completed_steps = 0
        total_actions = 0
        final_message: Optional[str] = None
        error: Optional[str] = None
        task_success = False
        is_done = False

        try:
            for step in range(max_steps):
                image = self._get_screenshot()
                screenshot_path = self._save_screenshot(image, step + 1)
                if screenshot_path:
                    screenshots.append(screenshot_path)
                image_b64 = self._encode_image(image)

                response_text = ""
                raw_response = None
                context_retry = False
                request_error: Optional[Exception] = None
                for attempt in range(max_attempts_per_step):
                    try:
                        response_text, context_retry, raw_response = self._call_llm(
                            instruction,
                            image_b64,
                        )
                        if not response_text:
                            raise RuntimeError("模型返回空响应")
                        request_error = None
                        break
                    except Exception as current_error:
                        request_error = current_error
                        logger.error(
                            "第 %s 步第 %s 次调用 OpenSource-UI-TRAS 失败: %s",
                            step + 1,
                            attempt + 1,
                            current_error,
                        )
                        if attempt < max_attempts_per_step - 1:
                            time.sleep(1.0)

                if request_error is not None:
                    raise OpenSourceUITRASInfrastructureError(
                        f"第 {step + 1} 步无法获取 OpenSource-UI-TRAS 响应: {request_error}"
                    ) from request_error

                action_record: Dict[str, Any] = {
                    "step": step + 1,
                    "response_text": response_text,
                    "raw_response": _response_to_dict(raw_response),
                    "context_retry": context_retry,
                    "screenshot": screenshot_path,
                    "parsed_actions": [],
                    "execution_results": [],
                    "parse_error": None,
                }
                executed_actions.append(action_record)
                completed_steps = step + 1

                try:
                    parsed_actions = self.official.parse_action(
                        response_text,
                        factor=1000,
                        origin_resized_height=image.height,
                        origin_resized_width=image.width,
                        model_type="qwen25vl",
                    )
                    if not parsed_actions:
                        raise ValueError("官方解析器未返回动作")
                    action_record["parsed_actions"] = parsed_actions
                except Exception as parse_error:
                    action_record["parse_error"] = str(parse_error)
                    error = f"第 {step + 1} 步无法解析模型响应: {parse_error}"
                    logger.error(error)
                    break

                self.history.append(
                    {
                        "image_b64": image_b64,
                        "assistant_content": response_text,
                    }
                )
                if self.history_turns:
                    self.history = self.history[-self.history_turns :]
                else:
                    self.history = []

                try:
                    for parsed_action in parsed_actions:
                        outcome = self.action_executor.execute(parsed_action)
                        total_actions += 1
                        action_record["execution_results"].append(
                            {
                                "action_type": parsed_action.get("action_type"),
                                "success": outcome.success,
                                "should_stop": outcome.should_stop,
                                "task_success": outcome.task_success,
                                "final_message": outcome.final_message,
                            }
                        )
                        if not outcome.success:
                            raise RuntimeError("动作执行器返回失败")
                        if outcome.should_stop:
                            is_done = True
                            task_success = outcome.task_success
                            final_message = outcome.final_message
                            if not task_success:
                                error = final_message or "任务未完成"
                            break
                except ValueError as action_error:
                    error = f"第 {step + 1} 步动作执行失败: {action_error}"
                    logger.error(error)
                    break
                except Exception as action_error:
                    raise OpenSourceUITRASInfrastructureError(
                        f"第 {step + 1} 步 Android 操作异常: {action_error}"
                    ) from action_error

                if is_done:
                    break
                time.sleep(self.wait_after_action_seconds)

            if not is_done and not error:
                error = f"达到最大步数限制 ({max_steps})，任务未完成"

            return AgentExecutionResult(
                success=task_success,
                completed_steps=completed_steps,
                total_actions=total_actions,
                executed_actions=executed_actions,
                screenshot_dir=task_folder,
                screenshots=screenshots,
                error=None if task_success else error,
                final_message=final_message,
            )
        except OpenSourceUITRASInfrastructureError:
            logger.exception("OpenSource-UI-TRAS 基础设施异常")
            raise
        except Exception as unexpected_error:
            logger.exception("OpenSource-UI-TRAS 执行异常: %s", unexpected_error)
            raise OpenSourceUITRASInfrastructureError(
                f"执行过程中发生基础设施异常: {unexpected_error}"
            ) from unexpected_error
        finally:
            self.current_task_folder = None
