# -*- coding: utf-8 -*-
"""M3A Agent - 基于 uiautomator2 和 OpenAI 的多模态 Android 自动化 Agent"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import numpy as np
from PIL import Image

from ..base import BaseAgent, AgentExecutionResult
from .u2_env import U2Env, UIElement
from .openai_wrapper import OpenAIWrapper
from .action_executor import ActionExecutor
from .m3a_utils import (
    validate_ui_element,
    add_ui_element_mark,
    add_screenshot_label,
    parse_reason_action_output,
)
from .prompt import (
    PROMPT_PREFIX,
    GUIDANCE,
    ACTION_SELECTION_PROMPT_TEMPLATE,
    SUMMARY_PROMPT_TEMPLATE,
)
import logging

logging.basicConfig(level=logging.INFO)


def _generate_ui_element_description(ui_element: UIElement, index: int) -> str:
    """生成 UI 元素的描述字符串."""
    element_description = f'UI element {index}: {{"index": {index}, '
    if ui_element.text:
        element_description += f'"text": "{ui_element.text}", '
    if ui_element.content_description:
        element_description += f'"content_description": "{ui_element.content_description}", '
    if ui_element.hint_text:
        element_description += f'"hint_text": "{ui_element.hint_text}", '
    if ui_element.tooltip:
        element_description += f'"tooltip": "{ui_element.tooltip}", '
    element_description += f'"is_clickable": {"True" if ui_element.is_clickable else "False"}, '
    element_description += f'"is_long_clickable": {"True" if ui_element.is_long_clickable else "False"}, '
    element_description += f'"is_editable": {"True" if ui_element.is_editable else "False"}, '
    if ui_element.is_scrollable:
        element_description += '"is_scrollable": True, '
    if ui_element.is_focusable:
        element_description += '"is_focusable": True, '
    element_description += f'"is_selected": {"True" if ui_element.is_selected else "False"}, '
    element_description += f'"is_checked": {"True" if ui_element.is_checked else "False"}, '
    return element_description[:-2] + "}"


def _generate_ui_elements_description_list(
    ui_elements: List[UIElement],
    screen_width_height_px: tuple[int, int],
) -> str:
    """生成 UI 元素列表的描述字符串."""
    tree_info = ""
    for index, ui_element in enumerate(ui_elements):
        if validate_ui_element(ui_element, screen_width_height_px):
            tree_info += _generate_ui_element_description(ui_element, index) + "\n"
    return tree_info


def _action_selection_prompt(
    goal: str,
    history: List[str],
    ui_elements: str,
    additional_guidelines: Optional[List[str]] = None,
) -> str:
    """生成动作选择提示词."""
    if history:
        history_str = "\n".join(history)
    else:
        history_str = "You just started, no action has been performed yet."

    extra_guidelines = ""
    if additional_guidelines:
        extra_guidelines = "For The Current Task:\n"
        for guideline in additional_guidelines:
            extra_guidelines += f"- {guideline}\n"

    return ACTION_SELECTION_PROMPT_TEMPLATE.format(
        prompt_prefix=PROMPT_PREFIX,
        goal=goal,
        history=history_str,
        ui_elements=ui_elements if ui_elements else "Not available",
        guidance=GUIDANCE,
        additional_guidelines=extra_guidelines,
    )


def _summarize_prompt(
    action: str,
    reason: str,
    goal: str,
    before_elements: str,
    after_elements: str,
) -> str:
    """生成总结提示词."""
    return SUMMARY_PROMPT_TEMPLATE.format(
        prompt_prefix=PROMPT_PREFIX,
        goal=goal,
        before_elements=before_elements,
        after_elements=after_elements,
        action=action,
        reason=reason,
    )


class M3AAgent(BaseAgent):
    """M3A Agent - 基于 uiautomator2 和 OpenAI 的多模态 Android 自动化 Agent"""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
        device_id: str,
        screenshots_dir: str = "screenshots",
        wait_after_action_seconds: float = 2.0,
        model_kwargs: Optional[dict] = None,
    ):
        """初始化 M3A Agent.

        Args:
            api_key: OpenAI API密钥（必需位置参数）
            base_url: OpenAI API基础URL（必需位置参数）
            model_name: OpenAI 模型名称（必需位置参数）
            device_id: 设备 ID（必需位置参数）
            screenshots_dir: 截图保存目录（可选关键字参数）
            wait_after_action_seconds: 执行动作后等待时间（秒）（可选关键字参数）
            model_kwargs: 传递给 chat.completions.create 的额外关键字参数（可选关键字参数）
        """
        # 创建截图目录
        self.screenshots_dir = screenshots_dir
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

        # 初始化环境
        self.env = U2Env(device_id)

        # 初始化 LLM wrapper
        self.llm = OpenAIWrapper(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            model_kwargs=model_kwargs,
        )

        # 初始化动作执行器
        self.action_executor = ActionExecutor(self.env.u2_device)

        # 历史记录
        self.history = []
        self.additional_guidelines = None
        self.wait_after_action_seconds = wait_after_action_seconds

        # 当前任务文件夹
        self.current_task_folder = None

    def set_task_guidelines(self, task_guidelines: List[str]) -> None:
        """设置任务特定的指导原则."""
        self.additional_guidelines = task_guidelines

    def reset(self):
        """重置 Agent."""
        self.history = []

    def _save_screenshot(self, screenshot: np.ndarray, step: int, prefix: str = "") -> Optional[str]:
        """保存截图到文件.

        Args:
            screenshot: 截图 numpy 数组
            step: 步骤编号
            prefix: 文件名前缀

        Returns:
            截图文件路径，如果保存失败则返回 None
        """
        try:
            if screenshot is None:
                return None

            # 确保数组值在 0-255 范围内
            if screenshot.dtype != np.uint8:
                screenshot = np.clip(screenshot, 0, 255).astype(np.uint8)

            image = Image.fromarray(screenshot)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{prefix}screenshot_step_{step}_{timestamp}.png"

            if self.current_task_folder:
                save_path = os.path.join(self.current_task_folder, filename)
            else:
                save_path = os.path.join(self.screenshots_dir, filename)

            # 保存图片
            image.save(save_path)
            return save_path
        except Exception as e:
            logging.error(f"保存截图失败: {e}")
            return None

    def step(self, goal: str) -> Dict[str, Any]:
        """执行一步操作（内部方法，参考 m3a.py 的实现）.

        Args:
            goal: 用户目标

        Returns:
            dict: 包含 done, data 的字典
        """
        step_data = {
            "raw_screenshot": None,
            "before_screenshot_with_som": None,
            "before_ui_elements": [],
            "after_screenshot_with_som": None,
            "action_prompt": None,
            "action_output": None,
            "action_output_json": None,
            "action_reason": None,
            "action_raw_response": None,
            "summary_prompt": None,
            "summary": None,
            "summary_raw_response": None,
        }

        logging.info(f"----------step {len(self.history) + 1}----------")

        # 获取当前状态
        state = self.env.get_state(wait_to_stabilize=True)
        logical_screen_size = self.env.logical_screen_size
        orientation = self.env.orientation
        physical_frame_boundary = self.env.physical_frame_boundary

        before_ui_elements = state["ui_elements"]
        step_data["before_ui_elements"] = before_ui_elements
        before_ui_elements_list = _generate_ui_elements_description_list(before_ui_elements, logical_screen_size)

        step_data["raw_screenshot"] = state["pixels"].copy()
        before_screenshot = state["pixels"].copy()

        logging.debug(f"Before screenshot shape: {before_screenshot.shape}")

        # 在截图上标记 UI 元素
        for index, ui_element in enumerate(before_ui_elements):
            if validate_ui_element(ui_element, logical_screen_size):
                add_ui_element_mark(
                    before_screenshot,
                    ui_element,
                    index,
                    logical_screen_size,
                    physical_frame_boundary,
                    orientation,
                )

        step_data["before_screenshot_with_som"] = before_screenshot.copy()
        logging.debug(f"Before screenshot with SOM shape: {step_data['before_screenshot_with_som'].shape}")

        # 生成动作选择提示词
        action_prompt = _action_selection_prompt(
            goal,
            ["Step " + str(i + 1) + "- " + step_info["summary"] for i, step_info in enumerate(self.history)],
            before_ui_elements_list,
            self.additional_guidelines,
        )
        step_data["action_prompt"] = action_prompt
        logging.debug(f"Action prompt: {action_prompt}")

        # 调用 LLM 选择动作
        action_output, is_safe, raw_response = self.llm.predict_mm(
            action_prompt,
            [
                step_data["raw_screenshot"],
                before_screenshot,
            ],
        )
        logging.debug(f"Action output: {action_output}, is_safe: {is_safe}")

        if is_safe == False:
            action_output = f"""Reason: Triggered LLM safety classifier.
Action: {{"action_type": "status", "goal_status": "infeasible"}}"""

        if not raw_response:
            logging.error("Error calling LLM in action selection phase.")
            raise RuntimeError("Error calling LLM in action selection phase.")

        step_data["action_output"] = action_output
        step_data["action_raw_response"] = raw_response

        logging.debug(f"Action output: {action_output}")

        # 解析 reason 和 action
        reason, action = parse_reason_action_output(action_output)
        logging.debug(f"Reason: {reason}, Action: {action}")

        # 如果输出格式不正确
        if (not reason) or (not action):
            logging.error("Action prompt output is not in the correct format.")
            step_data["summary"] = (
                "Output for action selection is not in the correct format, so no action is performed."
            )
            self.history.append(step_data)
            return {"done": False, "data": step_data}

        logging.debug(f"Action: {action}")
        logging.debug(f"Reason: {reason}")
        step_data["action_reason"] = reason

        # 解析 JSON action
        try:
            if not action:
                raise ValueError("Action string is empty")
            action_dict = json.loads(action)
            if not isinstance(action_dict, dict):
                raise ValueError(f"Parsed action is not a dict, got {type(action_dict)}")
            if "action_type" not in action_dict:
                raise ValueError(f"Action dict missing 'action_type' key: {action_dict}")
            step_data["action_output_json"] = action_dict
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logging.error("Failed to convert the output to a valid action.")
            logging.error(f"Error: {str(e)}")
            logging.error(f"Action string: {action}")
            step_data["summary"] = (
                "Can not parse the output to a valid action. Please make sure to pick"
                " the action from the list with required parameters (if any) in the"
                " correct JSON format!"
            )
            self.history.append(step_data)
            return {"done": False, "data": step_data}

        # 检查 index 是否有效
        action_type = action_dict.get("action_type")
        action_index = action_dict.get("index")
        num_ui_elements = len(before_ui_elements)
        if action_type in ["click", "long_press", "input_text", "scroll"] and action_index is not None:
            if action_index >= num_ui_elements:
                logging.error(
                    f"Index out of range, prediction index is {action_index}, but the"
                    f" UI element list only has {num_ui_elements} elements."
                )
                step_data["summary"] = (
                    "The parameter index is out of range. Remember the index must be in the UI element list!"
                )
                self.history.append(step_data)
                return {"done": False, "data": step_data}

            # 在原始截图上标记目标元素
            add_ui_element_mark(
                step_data["raw_screenshot"],
                before_ui_elements[action_index],
                action_index,
                logical_screen_size,
                physical_frame_boundary,
                orientation,
            )

        # 如果是 status 动作，直接返回
        if action_type == "status":
            goal_status = action_dict.get("goal_status")
            if goal_status == "infeasible":
                logging.info("Agent stopped since it thinks mission impossible.")
                step_data["summary"] = "Agent thinks the task is infeasible."
                step_data["final_message"] = "任务不可行"
            else:
                step_data["summary"] = "Agent thinks the request has been completed."
                step_data["final_message"] = "任务已完成"
            self.history.append(step_data)
            return {"done": True, "data": step_data}

        # 如果是 answer 动作，记录答案并完成
        if action_type == "answer":
            answer_text = action_dict.get("text", "")
            logging.info(f"Agent answered with: {answer_text}")
            step_data["summary"] = f"Agent answered: {answer_text}"
            step_data["final_message"] = answer_text
            self.history.append(step_data)
            return {"done": True, "data": step_data}

        # 执行动作
        try:
            self.action_executor.execute_action(action_dict, before_ui_elements)
        except Exception as e:
            logging.error("Failed to execute action.")
            logging.error(str(e))
            step_data["summary"] = (
                "Can not execute the action, make sure to select the action with"
                " the required parameters (if any) in the correct JSON format!"
            )
            return {"done": False, "data": step_data}

        # 等待界面稳定
        time.sleep(self.wait_after_action_seconds)

        # 获取执行后的状态
        state = self.env.get_state(wait_to_stabilize=False)
        logical_screen_size = self.env.logical_screen_size
        orientation = self.env.orientation
        physical_frame_boundary = self.env.physical_frame_boundary

        after_ui_elements = state["ui_elements"]
        after_ui_elements_list = _generate_ui_elements_description_list(after_ui_elements, logical_screen_size)
        after_screenshot = state["pixels"].copy()

        # 在截图上标记 UI 元素
        for index, ui_element in enumerate(after_ui_elements):
            if validate_ui_element(ui_element, logical_screen_size):
                add_ui_element_mark(
                    after_screenshot,
                    ui_element,
                    index,
                    logical_screen_size,
                    physical_frame_boundary,
                    orientation,
                )

        # 添加标签
        add_screenshot_label(step_data["before_screenshot_with_som"], "before")
        add_screenshot_label(after_screenshot, "after")
        step_data["after_screenshot_with_som"] = after_screenshot.copy()

        # 生成总结提示词
        summary_prompt = _summarize_prompt(
            action,
            reason,
            goal,
            before_ui_elements_list,
            after_ui_elements_list,
        )

        # 调用 LLM 生成总结
        summary, is_safe, raw_response = self.llm.predict_mm(
            summary_prompt,
            [
                step_data["before_screenshot_with_som"],
                after_screenshot,
            ],
        )

        if is_safe == False:
            summary = "Summary triggered LLM safety classifier."

        if not raw_response:
            logging.error(f"Error calling LLM in summarization phase. This should not happen: {summary}")
            step_data["summary"] = f"Some error occurred calling LLM during summarization phase: {summary}"
            self.history.append(step_data)
            return {"done": False, "data": step_data}

        step_data["summary_prompt"] = summary_prompt
        step_data["summary"] = f"Action selected: {action}. {summary}"
        logging.info(f"Summary: {summary}")
        step_data["summary_raw_response"] = raw_response

        self.history.append(step_data)
        return {"done": False, "data": step_data}

    def execute_instruction(
        self,
        instruction: str,
        max_steps: int = 50,
        max_attempts_per_step: int = 3,
    ) -> AgentExecutionResult:
        """执行指令（实现 BaseAgent 接口）.

        Args:
            instruction: 要执行的指令/目标
            max_steps: 最大执行步数
            max_attempts_per_step: 每步最大尝试次数（此参数在 M3A 中不使用，保留以兼容接口）

        Returns:
            AgentExecutionResult: 执行结果
        """
        logging.info(f"\n=== 开始执行任务: {instruction} ===")

        # 创建任务文件夹
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_instruction = instruction.replace("/", "_").replace("\\", "_").strip()[:50]
        task_folder_name = f"{timestamp}_{safe_instruction}"
        self.current_task_folder = os.path.join(self.screenshots_dir, task_folder_name)
        if not os.path.exists(self.current_task_folder):
            os.makedirs(self.current_task_folder)
        logging.debug(f"截图将保存到: {self.current_task_folder}")

        # 重置历史
        self.history = []

        executed_actions = []
        screenshots = []
        error = None
        completed_steps = 0

        try:
            # 执行步骤
            is_done = False
            for step in range(max_steps):
                logging.info(f"\n--- 第 {step + 1} 步 ---")
                logging.info(f"目标: {instruction}")

                # 执行一步
                response = self.step(instruction)

                # 保存截图
                step_data = response["data"]
                screenshot_path = None

                # 尝试保存原始截图
                if "raw_screenshot" in step_data and step_data["raw_screenshot"] is not None:
                    screenshot_path = self._save_screenshot(step_data["raw_screenshot"], step + 1, prefix="raw_")
                elif "before_screenshot_with_som" in step_data and step_data["before_screenshot_with_som"] is not None:
                    screenshot_path = self._save_screenshot(
                        step_data["before_screenshot_with_som"], step + 1, prefix="before_"
                    )

                if screenshot_path:
                    screenshots.append(screenshot_path)

                # 收集动作信息
                action_info: Dict[str, Any] = {
                    "step": step + 1,
                    "done": response["done"],
                    "summary": step_data.get("summary", ""),
                    "action_output": step_data.get("action_output", ""),
                    "action_reason": step_data.get("action_reason", ""),
                    "action_json": step_data.get("action_output_json", {}),
                    "screenshot": screenshot_path,
                }
                executed_actions.append(action_info)

                completed_steps = step + 1

                # 检查是否完成
                if response["done"]:
                    is_done = True
                    logging.info("任务完成！")
                    break
                else:
                    logging.info(f"步骤 {step + 1} 摘要: {step_data.get('summary', 'N/A')}")

            # 判断是否成功
            success = is_done
            final_message = None

            # 提取 final_message
            if is_done and executed_actions:
                # 从最后一步的 step_data 中获取 final_message
                last_step_data = response.get("data", {})
                final_message = last_step_data.get("final_message")
                # 如果没有 final_message，使用 summary
                if not final_message:
                    final_message = last_step_data.get("summary", "任务已完成")
            elif not is_done:
                error_msg = f"达到最大步数限制 ({max_steps})，任务未完成"
                logging.error(error_msg)
                if executed_actions:
                    # 使用最后一步的 summary 作为 final_message
                    last_action = executed_actions[-1]
                    final_message = last_action.get("summary", "任务未完成")

            return AgentExecutionResult(
                success=success,
                completed_steps=completed_steps,
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshots=screenshots,
                error=error,
                final_message=final_message,
            )

        except Exception as e:
            error_msg = f"执行过程中发生错误: {str(e)}"
            logging.error(error_msg)
            # 执行出错时，final_message 可以为 None
            return AgentExecutionResult(
                success=False,
                completed_steps=completed_steps,
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshots=screenshots,
                error=error_msg,
                final_message=None,
            )
        finally:
            # 清理
            self.current_task_folder = None

    def close(self):
        """关闭 Agent，释放资源"""
        if hasattr(self, "env") and self.env is not None:
            self.env.close()
