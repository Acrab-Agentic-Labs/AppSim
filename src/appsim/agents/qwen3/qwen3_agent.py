# -*- coding: utf-8 -*-
"""Qwen3 Agent - 基于 Qwen3-VL 和 uiautomator2 的移动端自动化 Agent"""

import base64
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import uiautomator2 as u2
from openai import OpenAI
from PIL import Image

from ..base import AgentExecutionResult, BaseAgent

SYSTEM_PROMPT_TEMPLATE = """

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.
* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.
* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.
* The screen's resolution is 999x999.
* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", \
"parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:
* `click`: Click the point on the screen with coordinate (x, y).
* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.
* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).
* `type`: Input the specified text into the activated input box.
* `answer`: Output the answer.
* `system_button`: Press the system button.
* `wait`: Wait specified seconds for the change to happen.
* `terminate`: Terminate the current task and report its completion status.", \
"enum": ["click", "long_press", "swipe", "type", "answer", "system_button", "wait", "terminate"], "type": "string"},\
"coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, \
"coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, \
"text": {"description": "Required only by `action=type` and `action=answer`.", "type": "string"}, \
"time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, \
"button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, \
"status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Thought: one concise sentence explaining the next move (no multi-step reasoning).
2) Action: a short imperative describing what to do in the UI.
3) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Thought, Action, <tool_call>.
- Be brief: one sentence for Thought, one for Action.
- Do not output anything else outside those three parts.
- If finishing, use action=terminate in the tool call.
"""

USER_PROMPT_TEMPLATE = """
The user query: {instruction}.
Task progress (You have done the following operation on the current device): {stage2_history}.
"""


def rescale_coordinates(point: List[int], width: int, height: int) -> List[int]:
    """将 999x999 虚拟坐标缩放到实际屏幕尺寸

    Args:
        point: [x, y] 坐标（虚拟坐标，范围 0-999）
        width: 实际屏幕宽度
        height: 实际屏幕高度

    Returns:
        [x, y] 实际坐标
    """
    return [round(point[0] / 999 * width), round(point[1] / 999 * height)]


def encode_image(image: np.ndarray) -> str:
    """将 numpy 数组编码为 base64 字符串

    Args:
        image: numpy 数组图像

    Returns:
        base64 编码的字符串
    """
    if image.dtype != np.uint8:
        image = np.clip(image, 0, 255).astype(np.uint8)

    pil_image = Image.fromarray(image)

    # 转换为 JPEG bytes
    import io

    in_mem_file = io.BytesIO()
    pil_image.save(in_mem_file, format="JPEG")
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    return base64.b64encode(img_bytes).decode("utf-8")


class Qwen3Agent(BaseAgent):
    """Qwen3 Agent - 基于 Qwen3-VL 和 uiautomator2 的移动端自动化 Agent"""

    def __init__(
        self,
        model_name: str,
        api_key: str,
        api_base: str,
        device_id: str,
        screenshots_dir: str = "screenshots",
        wait_after_action_seconds: float = 2.0,
        model_kwargs: Optional[dict] = None,
    ):
        """初始化 Qwen3 Agent

        Args:
            model_name: 模型名称（必需位置参数）
            api_key: API 密钥（必需位置参数）
            api_base: API 基础 URL（必需位置参数）
            device_id: 设备 ID（必需位置参数）
            screenshots_dir: 截图保存目录（可选关键字参数）
            wait_after_action_seconds: 执行动作后等待时间（秒）（可选关键字参数）
            model_kwargs: 传递给 chat.completions.create 的额外关键字参数（可选关键字参数）
        """
        self.model_name = model_name
        self.api_key = api_key
        self.api_base = api_base
        self.device_id = device_id
        self.screenshots_dir = screenshots_dir
        self.wait_after_action_seconds = wait_after_action_seconds
        self.model_kwargs = model_kwargs or {}

        # 创建截图目录
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

        # 初始化 OpenAI 客户端
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)

        # 初始化 uiautomator2 设备连接
        self.u2_device = None
        self._check_and_connect()

        # 历史记录
        self.history = []

        # 当前任务文件夹
        self.current_task_folder = None

    def _check_and_connect(self):
        """检查并连接设备"""
        try:
            self.u2_device = u2.connect(self.device_id)
            info = self.u2_device.info
            logging.info("✅ uiautomator2 连接成功!")
            logging.info(f"   设备: {self.device_id}")
            logging.info(f"   屏幕尺寸: {info.get('displayWidth', 'Unknown')}x{info.get('displayHeight', 'Unknown')}")
        except Exception as e:
            logging.error(f"uiautomator2 连接失败: {e}")
            raise RuntimeError(f"uiautomator2 连接失败: {e}")

    def reset(self) -> None:
        """重置 Agent"""
        self.history = []

    def _save_screenshot(self, screenshot: np.ndarray, step: int, prefix: str = "") -> Optional[str]:
        """保存截图到文件

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
            logging.debug(f"保存截图: {save_path}")
            return save_path
        except Exception as e:
            logging.error(f"保存截图失败: {e}")
            return None

    def _get_screenshot(self) -> np.ndarray:
        """获取当前屏幕截图

        Returns:
            截图 numpy 数组
        """
        screenshot = self.u2_device.screenshot()
        return np.array(screenshot)

    def _get_screen_size(self) -> tuple[int, int]:
        """获取屏幕尺寸

        Returns:
            (width, height) 元组
        """
        info = self.u2_device.info
        return (info.get("displayWidth", 1080), info.get("displayHeight", 1920))

    def _parse_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """解析 Qwen3 的响应，提取 tool_call

        Args:
            response_text: LLM 返回的文本

        Returns:
            解析后的 action 字典，如果解析失败则返回 None
        """
        try:
            # 提取 <tool_call>...</tool_call> 中的 JSON
            if "<tool_call>" not in response_text or "</tool_call>" not in response_text:
                logging.error("响应中未找到 <tool_call> 标签")
                return None

            # 提取 tool_call 内容（兼容换行符的情况）
            # 示例代码使用: output_text.split('<tool_call>\n')[1].split('\n</tool_call>')[0]
            if "<tool_call>\n" in response_text:
                tool_call_content = response_text.split("<tool_call>\n")[1].split("\n</tool_call>")[0]
            else:
                tool_call_start = response_text.find("<tool_call>")
                tool_call_end = response_text.find("</tool_call>")

                if tool_call_start == -1 or tool_call_end == -1:
                    logging.error("无法找到完整的 <tool_call> 标签")
                    return None

                tool_call_content = response_text[tool_call_start + len("<tool_call>") : tool_call_end].strip()

            # 去除前后空白字符
            tool_call_content = tool_call_content.strip()

            # 解析 JSON
            tool_call_json = json.loads(tool_call_content)

            # 提取 arguments
            if "name" not in tool_call_json or "arguments" not in tool_call_json:
                logging.error("tool_call JSON 格式不正确")
                return None

            logging.debug(f"解析 tool_call 成功: {tool_call_json['arguments']}")
            return tool_call_json["arguments"]
        except json.JSONDecodeError as e:
            logging.error(f"解析 JSON 失败: {e}")
            logging.debug(f"响应内容: {response_text}")
            return None
        except Exception as e:
            logging.error(f"解析响应失败: {e}")
            import traceback

            traceback.print_exc()
            return None

    def _execute_action(self, action_dict: Dict[str, Any]) -> bool:
        """执行动作

        Args:
            action_dict: 动作字典，包含 action 和其他参数

        Returns:
            是否执行成功
        """
        try:
            action = action_dict.get("action")
            if not action:
                logging.error("动作缺少 'action' 字段")
                return False

            screen_width, screen_height = self._get_screen_size()

            if action == "click":
                coordinate = action_dict.get("coordinate")
                if not coordinate:
                    logging.error("click 动作缺少 coordinate 参数")
                    return False

                # 缩放坐标
                x, y = rescale_coordinates(coordinate, screen_width, screen_height)
                self.u2_device.click(x, y)
                logging.debug(f"点击坐标: ({x}, {y})")
                return True

            elif action == "long_press":
                coordinate = action_dict.get("coordinate")
                time_seconds = action_dict.get("time", 1.0)

                if not coordinate:
                    logging.error("long_press 动作缺少 coordinate 参数")
                    return False

                # 缩放坐标
                x, y = rescale_coordinates(coordinate, screen_width, screen_height)
                self.u2_device.long_click(x, y, duration=time_seconds)
                logging.debug(f"长按坐标: ({x}, {y}), 持续时间: {time_seconds}秒")
                return True

            elif action == "swipe":
                coordinate = action_dict.get("coordinate")
                coordinate2 = action_dict.get("coordinate2")

                if not coordinate or not coordinate2:
                    logging.error("swipe 动作缺少 coordinate 或 coordinate2 参数")
                    return False

                # 缩放坐标
                x1, y1 = rescale_coordinates(coordinate, screen_width, screen_height)
                x2, y2 = rescale_coordinates(coordinate2, screen_width, screen_height)
                self.u2_device.swipe(x1, y1, x2, y2, duration=0.5)
                logging.debug(f"滑动: ({x1}, {y1}) -> ({x2}, {y2})")
                return True

            elif action == "type":
                text = action_dict.get("text")
                if not text:
                    logging.error("type 动作缺少 text 参数")
                    return False

                self.u2_device.set_fastinput_ime()
                self.u2_device.send_keys(text)
                logging.debug(f"输入文本: {text}")
                return True

            elif action == "answer":
                text = action_dict.get("text", "")
                logging.info(f"回答: {text}")
                return True  # answer 不需要执行实际动作

            elif action == "system_button":
                button = action_dict.get("button")
                if not button:
                    logging.error("system_button 动作缺少 button 参数")
                    return False

                # 映射按钮名称
                button_mapping = {
                    "Back": "back",
                    "Home": "home",
                    "Menu": "menu",
                    "Enter": "enter",
                }

                button_key = button_mapping.get(button)
                if not button_key:
                    logging.error(f"未知的系统按钮: {button}")
                    return False

                self.u2_device.press(button_key)
                logging.debug(f"按下系统按钮: {button}")
                return True

            elif action == "wait":
                wait_time = action_dict.get("time", 1.0)
                time.sleep(wait_time)
                logging.debug(f"等待 {wait_time} 秒")
                return True

            elif action == "terminate":
                status = action_dict.get("status", "success")
                logging.info(f"终止任务，状态: {status}")
                return True  # terminate 不需要执行实际动作

            else:
                logging.error(f"未知的动作类型: {action}")
                return False

        except Exception as e:
            logging.error(f"执行动作时出错: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _call_llm(self, instruction: str, screenshot: np.ndarray) -> Optional[str]:
        """调用 LLM 获取下一步动作

        Args:
            instruction: 用户指令
            screenshot: 当前屏幕截图

        Returns:
            LLM 返回的文本，如果失败则返回 None
        """
        try:
            # 构建历史记录字符串
            stage2_history = ""
            newline = chr(10)
            carriage_return = chr(13)
            for idx, his in enumerate(self.history):
                cleaned_his = his.replace(newline, "").replace(carriage_return, "").replace('"', "")
                stage2_history += f"Step {idx + 1}: {cleaned_his}; "

            # 构建用户查询
            user_query = USER_PROMPT_TEMPLATE.format(instruction=instruction, stage2_history=stage2_history)

            # 编码图像
            base64_image = encode_image(screenshot)

            # 构建消息
            messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": SYSTEM_PROMPT_TEMPLATE},
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_query},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                },
            ]

            # 调用 LLM
            completion = self.client.chat.completions.create(
                model=self.model_name, messages=messages, **self.model_kwargs
            )

            output_text = completion.choices[0].message.content
            logging.debug(f"LLM 响应: {output_text[:200]}...")  # 只记录前200字符
            return output_text

        except Exception as e:
            logging.error(f"调用 LLM 失败: {e}")
            import traceback

            traceback.print_exc()
            return None

    def execute_instruction(
        self,
        instruction: str,
        max_steps: int = 50,
        max_attempts_per_step: int = 3,
    ) -> AgentExecutionResult:
        """执行指令（实现 BaseAgent 接口）

        Args:
            instruction: 要执行的指令/目标
            max_steps: 最大执行步数
            max_attempts_per_step: 每步最大尝试次数

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
        logging.info(f"截图将保存到: {self.current_task_folder}")

        # 重置历史
        self.history = []

        executed_actions = []
        screenshots = []
        error = None
        completed_steps = 0
        final_message = None

        try:
            # 执行步骤
            is_done = False
            for step in range(max_steps):
                logging.info(f"\n--- 第 {step + 1} 步 ---")
                logging.info(f"目标: {instruction}")

                # 获取当前截图
                screenshot = self._get_screenshot()
                screenshot_path = self._save_screenshot(screenshot, step + 1, prefix="")
                if screenshot_path:
                    screenshots.append(screenshot_path)

                # 调用 LLM 获取下一步动作
                response_text = None
                for attempt in range(max_attempts_per_step):
                    response_text = self._call_llm(instruction, screenshot)
                    if response_text:
                        break
                    logging.warning(f"第 {attempt + 1} 次尝试失败，重试...")
                    time.sleep(1)

                if not response_text:
                    error = f"第 {step + 1} 步：无法获取 LLM 响应"
                    logging.error(f"错误: {error}")
                    break

                # 解析响应
                action_dict = self._parse_response(response_text)
                if not action_dict:
                    error = f"第 {step + 1} 步：无法解析 LLM 响应"
                    logging.error(f"错误: {error}")
                    # 尝试提取 Thought 和 Action 作为历史记录
                    if "Thought:" in response_text:
                        thought = response_text.split("Thought:")[1].split("\n")[0].strip()
                        self.history.append(thought)
                    break

                # 提取动作信息
                action = action_dict.get("action", "unknown")

                # 收集动作信息
                action_info: Dict[str, Any] = {
                    "step": step + 1,
                    "action": action,
                    "action_dict": action_dict,
                    "response_text": response_text,
                    "screenshot": screenshot_path,
                }
                executed_actions.append(action_info)

                # 检查是否终止
                if action == "terminate":
                    is_done = True
                    status = action_dict.get("status", "success")
                    final_message = None
                    logging.info(f"任务终止，状态: {status}")
                    break

                # 检查是否是回答
                if action == "answer":
                    is_done = True
                    answer_text = action_dict.get("text", "")
                    final_message = answer_text
                    logging.info(f"任务完成，回答: {answer_text}")
                    break

                # 执行动作
                success = self._execute_action(action_dict)
                if not success:
                    logging.error("动作执行失败")

                # 等待界面稳定
                time.sleep(self.wait_after_action_seconds)

                # 提取 Thought 和 Action 作为历史记录
                if "Thought:" in response_text:
                    thought = response_text.split("Thought:")[1].split("\n")[0].strip()
                    self.history.append(thought)
                elif "Action:" in response_text:
                    action_desc = response_text.split("Action:")[1].split("\n")[0].strip()
                    self.history.append(action_desc)

                completed_steps = step + 1

                # 打印当前步骤摘要
                if "Thought:" in response_text:
                    thought = response_text.split("Thought:")[1].split("\n")[0].strip()
                    logging.info(f"思考: {thought}")
                if "Action:" in response_text:
                    action_desc = response_text.split("Action:")[1].split("\n")[0].strip()
                    logging.info(f"动作: {action_desc}")

            # 判断是否成功
            final_success = is_done

            if not is_done:
                if not error:
                    error = f"达到最大步数限制 ({max_steps})，任务未完成"
                logging.warning(f"警告: {error}")
                final_message = None

            return AgentExecutionResult(
                success=final_success,
                completed_steps=completed_steps,
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshot_dir=self.current_task_folder if self.current_task_folder else self.screenshots_dir,
                screenshots=screenshots,
                error=error,
                final_message=final_message,
            )

        except Exception as e:
            error_msg = f"执行过程中发生错误: {str(e)}"
            logging.error(f"错误: {error_msg}")
            import traceback

            traceback.print_exc()
            return AgentExecutionResult(
                success=False,
                completed_steps=completed_steps,
                total_actions=len(executed_actions),
                executed_actions=executed_actions,
                screenshot_dir=self.current_task_folder if self.current_task_folder else self.screenshots_dir,
                screenshots=screenshots,
                error=error_msg,
                final_message=None,
            )
        finally:
            # 清理
            self.current_task_folder = None
