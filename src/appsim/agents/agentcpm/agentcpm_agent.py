# -*- coding: utf-8 -*-
"""AgentCPM-GUI Agent - 基于官方 VLLM Chat Completions 方案的移动端自动化 Agent。"""

import base64
import io
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import uiautomator2 as u2
from openai import OpenAI
from PIL import Image

from ..base import AgentExecutionResult, BaseAgent
from .action_utils import (
    CONTINUE_STATUSES,
    DEFAULT_DURATION_MS,
    FAILURE_STATUSES,
    LONG_PRESS_THRESHOLD_MS,
    SUCCESS_STATUSES,
    clamp,
    extract_json_object,
    rescale_point,
    validate_agentcpm_action,
)
from .prompt import build_system_prompt, build_user_text

logger = logging.getLogger(__name__)

MAX_IMAGE_LONG_SIDE = 1120


def is_context_length_error(error: Exception) -> bool:
    """判断是否为 VLLM/OpenAI 兼容接口返回的上下文长度错误。"""
    message = str(error).lower()
    return "maximum context length" in message or "context length" in message or "max_model_len" in message


def response_to_dict(response: Any) -> Optional[Dict[str, Any]]:
    """将 OpenAI SDK 响应转换为可 JSON 序列化的 dict。"""
    if response is None:
        return None
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if isinstance(response, dict):
        return response
    return {"repr": repr(response)}


class AgentCPMAgent(BaseAgent):
    """AgentCPM-GUI 移动端自动化 Agent。"""

    def __init__(
        self,
        api_key: str,
        api_base: str,
        model_name: str,
        device_id: str,
        screenshots_dir: str = "screenshots",
        wait_after_action_seconds: float = 2.0,
        max_tokens: int = 512,
        history_image_turns: int = 1,
        model_kwargs: Optional[dict] = None,
    ):
        if not api_base:
            raise ValueError("AgentCPM-GUI requires AGENTCPM_GUI_API_BASE or API_BASE")
        if history_image_turns > 1:
            raise ValueError("AGENTCPM_GUI_HISTORY_IMAGE_TURNS 不能大于 1")
        if history_image_turns < 0:
            raise ValueError("AGENTCPM_GUI_HISTORY_IMAGE_TURNS 不能小于 0")
        if max_tokens <= 0:
            raise ValueError("AGENTCPM_GUI_MAX_TOKENS 必须为正整数")

        self.api_key = api_key or "EMPTY"
        self.api_base = api_base
        self.model_name = model_name or "AgentCPM-GUI"
        self.device_id = device_id
        self.screenshots_dir = screenshots_dir
        self.wait_after_action_seconds = wait_after_action_seconds
        self.max_tokens = max_tokens
        self.history_image_turns = history_image_turns
        self.model_kwargs = model_kwargs or {}
        self.system_prompt = build_system_prompt()

        os.makedirs(self.screenshots_dir, exist_ok=True)
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)
        self.u2_device = u2.connect(self.device_id)
        self.history: List[Dict[str, str]] = []
        self.current_task_folder: Optional[str] = None

        info = self.u2_device.info
        logger.info("AgentCPM-GUI uiautomator2 连接成功: %s", self.device_id)
        logger.info("屏幕尺寸: %sx%s", info.get("displayWidth", "Unknown"), info.get("displayHeight", "Unknown"))

    def reset(self) -> None:
        """重置 Agent 历史。"""
        self.history = []

    def _get_screenshot(self) -> np.ndarray:
        screenshot = self.u2_device.screenshot()
        return np.array(screenshot.convert("RGB"))

    def _get_screen_size(self) -> Tuple[int, int]:
        info = self.u2_device.info
        return info.get("displayWidth", 1080), info.get("displayHeight", 1920)

    def _save_screenshot(self, screenshot: np.ndarray, step: int) -> Optional[str]:
        try:
            if screenshot.dtype != np.uint8:
                screenshot = np.clip(screenshot, 0, 255).astype(np.uint8)
            image = Image.fromarray(screenshot)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"screenshot_step_{step}_{timestamp}.png"
            save_dir = self.current_task_folder or self.screenshots_dir
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)
            return save_path
        except Exception as e:
            logger.error("保存截图失败: %s", e)
            return None

    def _encode_image(self, screenshot: np.ndarray) -> str:
        if screenshot.dtype != np.uint8:
            screenshot = np.clip(screenshot, 0, 255).astype(np.uint8)
        image = Image.fromarray(screenshot).convert("RGB")
        image = self._resize_for_agentcpm(image)
        with io.BytesIO() as in_mem_file:
            image.save(in_mem_file, format="JPEG")
            return base64.b64encode(in_mem_file.getvalue()).decode("utf-8")

    @staticmethod
    def _resize_for_agentcpm(image: Image.Image) -> Image.Image:
        width, height = image.size
        if max(width, height) <= MAX_IMAGE_LONG_SIDE:
            return image
        if height >= width:
            new_height = MAX_IMAGE_LONG_SIDE
            new_width = int(width * MAX_IMAGE_LONG_SIDE / height)
        else:
            new_width = MAX_IMAGE_LONG_SIDE
            new_height = int(height * MAX_IMAGE_LONG_SIDE / width)
        return image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)

    def _image_content(self, image_b64: str) -> Dict[str, Any]:
        return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}

    def _build_messages(self, instruction: str, current_image_b64: str, include_history: bool) -> List[Dict[str, Any]]:
        messages: List[Dict[str, Any]] = [{"role": "system", "content": self.system_prompt}]
        if include_history and self.history_image_turns > 0 and self.history:
            for turn in self.history[-self.history_image_turns :]:
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": build_user_text(instruction)},
                            self._image_content(turn["image_b64"]),
                        ],
                    }
                )
                messages.append({"role": "assistant", "content": turn["assistant_content"]})

        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": build_user_text(instruction)},
                    self._image_content(current_image_b64),
                ],
            }
        )
        return messages

    def _call_llm(self, instruction: str, image_b64: str) -> Tuple[str, bool, Any]:
        messages = self._build_messages(instruction, image_b64, include_history=True)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.1,
                top_p=0.3,
                max_tokens=self.max_tokens,
                **self.model_kwargs,
            )
            return response.choices[0].message.content or "", False, response
        except Exception as e:
            if not is_context_length_error(e):
                raise
            logger.warning("AgentCPM-GUI 上下文过长，降级为无历史截图并将 max_tokens 降为 256 后重试")

        retry_messages = self._build_messages(instruction, image_b64, include_history=False)
        retry_max_tokens = min(256, self.max_tokens)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=retry_messages,
            temperature=0.1,
            top_p=0.3,
            max_tokens=retry_max_tokens,
            **self.model_kwargs,
        )
        return response.choices[0].message.content or "", True, response

    def _execute_action(self, action: Dict[str, Any]) -> Tuple[bool, bool, bool, Optional[str]]:
        """执行动作，返回 (执行成功, 是否停止, 任务是否成功, 最终消息)。"""
        validate_agentcpm_action(action)

        status = action.get("STATUS", "continue")
        action_success = True
        final_message = action.get("thought")

        if "POINT" in action:
            action_success = self._execute_point_action(action)
        elif "PRESS" in action:
            action_success = self._execute_press(action["PRESS"])
        elif "TYPE" in action:
            action_success = self._execute_type(action["TYPE"])
        elif "duration" in action and status in CONTINUE_STATUSES:
            time.sleep(action["duration"] / 1000)

        if status in SUCCESS_STATUSES:
            return action_success, True, True, final_message or "任务已完成"
        if status in FAILURE_STATUSES:
            return action_success, True, False, final_message or f"任务停止: {status}"
        return action_success, False, False, final_message

    def _execute_point_action(self, action: Dict[str, Any]) -> bool:
        width, height = self._get_screen_size()
        x, y = rescale_point(action["POINT"], width, height)
        duration_ms = action.get("duration", DEFAULT_DURATION_MS)

        if "to" not in action:
            if duration_ms > LONG_PRESS_THRESHOLD_MS:
                self.u2_device.long_click(x, y, duration=duration_ms / 1000)
                logger.debug("长按坐标: (%s, %s), duration=%sms", x, y, duration_ms)
            else:
                self.u2_device.click(x, y)
                logger.debug("点击坐标: (%s, %s)", x, y)
            return True

        to = action["to"]
        if isinstance(to, list):
            x2, y2 = rescale_point(to, width, height)
        else:
            x2, y2 = self._direction_target(x, y, to, width, height)
        self.u2_device.swipe(x, y, x2, y2, duration=max(duration_ms, DEFAULT_DURATION_MS) / 1000)
        logger.debug("滑动: (%s, %s) -> (%s, %s)", x, y, x2, y2)
        return True

    def _direction_target(self, x: int, y: int, direction: str, width: int, height: int) -> Tuple[int, int]:
        distance = min(width, height) // 3
        if direction == "up":
            return x, clamp(y - distance, 0, height - 1)
        if direction == "down":
            return x, clamp(y + distance, 0, height - 1)
        if direction == "left":
            return clamp(x - distance, 0, width - 1), y
        if direction == "right":
            return clamp(x + distance, 0, width - 1), y
        raise ValueError(f"未知滑动方向: {direction}")

    def _execute_press(self, key: str) -> bool:
        key_mapping = {"HOME": "home", "BACK": "back", "ENTER": "enter"}
        self.u2_device.press(key_mapping[key])
        logger.debug("按下系统按键: %s", key)
        return True

    def _execute_type(self, text: str) -> bool:
        self.u2_device.set_fastinput_ime()
        self.u2_device.send_keys(text)
        logger.debug("输入文本: %s", text)
        return True

    def execute_instruction(
        self,
        instruction: str,
        max_steps: int = 50,
        max_attempts_per_step: int = 3,
    ) -> AgentExecutionResult:
        logger.info("\n=== 开始执行 AgentCPM-GUI 任务: %s ===", instruction)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_instruction = instruction.replace("/", "_").replace("\\", "_").strip()[:50]
        self.current_task_folder = os.path.join(self.screenshots_dir, f"{timestamp}_{safe_instruction}")
        os.makedirs(self.current_task_folder, exist_ok=True)

        self.history = []
        executed_actions: List[Dict[str, Any]] = []
        screenshots: List[str] = []
        completed_steps = 0
        final_message: Optional[str] = None
        error: Optional[str] = None
        is_done = False
        task_success = False

        try:
            for step in range(max_steps):
                screenshot = self._get_screenshot()
                screenshot_path = self._save_screenshot(screenshot, step + 1)
                if screenshot_path:
                    screenshots.append(screenshot_path)

                image_b64 = self._encode_image(screenshot)
                response_text = None
                context_retry = False
                raw_response = None

                for attempt in range(max_attempts_per_step):
                    try:
                        response_text, context_retry, raw_response = self._call_llm(instruction, image_b64)
                        break
                    except Exception as e:
                        logger.error("第 %s 步第 %s 次调用 AgentCPM-GUI 失败: %s", step + 1, attempt + 1, e)
                        if attempt < max_attempts_per_step - 1:
                            time.sleep(1)

                if not response_text:
                    error = f"第 {step + 1} 步无法获取 AgentCPM-GUI 响应"
                    logger.error(error)
                    break

                action_dict: Dict[str, Any] = {}
                parse_error = None
                try:
                    action_dict = extract_json_object(response_text)
                    validate_agentcpm_action(action_dict)
                except Exception as e:
                    parse_error = str(e)
                    error = f"第 {step + 1} 步无法解析 AgentCPM-GUI 响应: {parse_error}"
                    logger.error(error)

                action_info: Dict[str, Any] = {
                    "step": step + 1,
                    "response_text": response_text,
                    "action_dict": action_dict,
                    "raw_response": response_to_dict(raw_response),
                    "context_retry": context_retry,
                    "screenshot": screenshot_path,
                    "parse_error": parse_error,
                }
                executed_actions.append(action_info)
                completed_steps = step + 1

                if parse_error:
                    break

                self.history.append({"image_b64": image_b64, "assistant_content": response_text})
                self.history = self.history[-self.history_image_turns :] if self.history_image_turns else []

                try:
                    action_success, should_stop, step_success, step_message = self._execute_action(action_dict)
                except Exception as e:
                    error = f"第 {step + 1} 步动作执行失败: {e}"
                    logger.error(error)
                    break

                action_info["execution_success"] = action_success
                if not action_success:
                    error = f"第 {step + 1} 步动作执行失败"
                    logger.error(error)
                    break

                if should_stop:
                    is_done = True
                    task_success = step_success
                    final_message = step_message
                    break

                time.sleep(self.wait_after_action_seconds)

            if not is_done and not error:
                error = f"达到最大步数限制 ({max_steps})，任务未完成"

            return AgentExecutionResult(
                success=task_success,
                completed_steps=completed_steps,
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshot_dir=self.current_task_folder,
                screenshots=screenshots,
                error=None if task_success else error,
                final_message=final_message,
            )
        except Exception as e:
            error_msg = f"执行过程中发生错误: {e}"
            logger.error(error_msg)
            return AgentExecutionResult(
                success=False,
                completed_steps=completed_steps,
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshot_dir=self.current_task_folder or self.screenshots_dir,
                screenshots=screenshots,
                error=error_msg,
                final_message=None,
            )
        finally:
            self.current_task_folder = None

    def close(self) -> None:
        """关闭 Agent。"""
        pass
