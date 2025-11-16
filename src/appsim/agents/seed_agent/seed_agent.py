import os
import time
import re
import json
import logging
from datetime import datetime
from PIL import Image
import base64
import uiautomator2 as u2

from appsim.tasks import AppEnum, APP_TASKS_MAP
from .prompt import PHONE_USE_DOUBAO
from .action_parser import ActionParser
from openai import OpenAI

from ..base import AgentExecutionResult, BaseAgent


class SeedAgent(BaseAgent):
    """真实手机/模拟器控制器"""

    def __init__(self, api_key, base_url, model_name, device_id, screenshots_dir="screenshots", model_kwargs=None):
        """
        初始化控制器

        Args:
            api_key: OpenAI API密钥（必需位置参数）
            base_url: OpenAI API基础URL（必需位置参数）
            model_name: 模型名称（必需位置参数）
            device_id: 设备ID（必需位置参数）
            screenshots_dir: 截图保存目录（可选关键字参数）
            model_kwargs: 传递给 chat.completions.create 的额外关键字参数（可选关键字参数）
        """
        # 初始化 logger
        self.logger = logging.getLogger(__name__)

        # 保存API配置参数
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.model_kwargs = model_kwargs or {}

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        # 设备ID
        self.device_id = device_id

        # 初始化 uiautomator2 设备连接
        self.u2_device = None

        # 创建screenshots文件夹
        self.screenshots_dir = screenshots_dir
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

        # 对话历史
        self.conversation_messages = []

        # AI动作解析器
        self.action_parser = ActionParser()

        # 当前任务文件夹
        self.current_task_folder = None

        # 检查ADB连接
        self._check_adb_connection()

    def reset(self) -> None:
        pass

    def execute_instruction(self, instruction, max_steps=50, max_attempts_per_step=3) -> AgentExecutionResult:
        """
        执行完整的指令流程：支持多步骤操作循环

        Args:
            instruction: 操作指令
            max_steps: 最大步骤数
            max_attempts_per_step: 每个步骤的最大尝试次数

        Returns:
            dict: 执行结果
        """
        self.logger.info(f"\n=== 开始执行任务: {instruction} ===")

        # 创建任务文件夹
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_instruction = re.sub(r"[^\w\s-]", "", instruction).strip()[:20]  # 清理指令名称
        task_folder_name = f"{timestamp}_{safe_instruction}"
        self.current_task_folder = os.path.join(self.screenshots_dir, task_folder_name)
        if not os.path.exists(self.current_task_folder):
            os.makedirs(self.current_task_folder)
        self.logger.debug(f"截图将保存到: {self.current_task_folder}")

        executed_actions = []
        screenshots = []

        for step in range(max_steps):
            self.logger.info(f"\n--- 第 {step + 1} 步 ---")

            step_success = False
            for attempt in range(max_attempts_per_step):
                try:
                    self.logger.debug(f"尝试 {attempt + 1}/{max_attempts_per_step}")

                    # 1. 截取当前屏幕
                    screenshot_path = self.capture_screen(step=step + 1, attempt=attempt + 1)
                    screenshots.append(screenshot_path)

                    # 2. 获取AI分析结果
                    self.logger.debug("正在分析屏幕...")
                    ai_response = self.get_ai_action(instruction, image_path=screenshot_path)
                    self.logger.debug(f"AI响应: {ai_response}")

                    # 3. 解析动作
                    actions = self.parse_ai_actions(ai_response)
                    if not actions:
                        self.logger.warning("未能解析到有效动作")
                        if attempt < max_attempts_per_step - 1:
                            self.logger.debug("等待后重试...")
                            time.sleep(1)
                            continue
                        else:
                            break

                    # 4. 执行动作
                    step_executed_actions = []
                    for action in actions:
                        self.logger.debug(f"执行动作: {action}")

                        # 检查是否为完成动作
                        if action.get("action") == "finished":
                            executed_actions.extend(step_executed_actions)
                            executed_actions.append(action)
                            self.logger.info(f"\n=== 任务完成: {action.get('content', '操作完成')} ===")
                            return AgentExecutionResult(
                                success=True,
                                completed_steps=step + 1,
                                total_actions=len(executed_actions),
                                executed_actions=executed_actions,
                                screenshots=screenshots,
                                final_message=action.get("content", "操作完成"),
                            )

                        # 执行动作
                        if self.execute_action(action):
                            step_executed_actions.append(action)
                            # 等待操作完成
                            time.sleep(2)
                        else:
                            self.logger.warning(f"动作执行失败: {action}")
                            break

                    if step_executed_actions:
                        executed_actions.extend(step_executed_actions)
                        step_success = True
                        break

                except Exception as e:
                    self.logger.error(f"步骤执行出错: {e}")
                    if attempt < max_attempts_per_step - 1:
                        self.logger.warning("等待后重试...")
                        time.sleep(1)

            if not step_success:
                self.logger.error(f"第 {step + 1} 步执行失败，任务终止")
                break

            # 检查是否应该继续
            if step >= max_steps - 1:
                self.logger.warning("达到最大步骤数，任务终止")
                break

        return AgentExecutionResult(
            success=False if not executed_actions else True,
            completed_steps=step + 1 if step_success else step,
            total_actions=len(executed_actions),
            executed_actions=executed_actions,
            screenshots=screenshots,
            error="未完成所有操作" if executed_actions else "执行失败",
        )

    def _check_adb_connection(self):
        """检查ADB连接状态"""
        # 初始化 uiautomator2 连接
        try:
            self.logger.info(f"正在尝试连接 uiautomator2 到设备: {self.device_id}")
            self.u2_device = u2.connect(self.device_id)

            # 测试连接是否正常
            info = self.u2_device.info
            self.logger.info(f"✅ uiautomator2 连接成功!")
            self.logger.info(f"   设备型号: {info.get('productName', 'Unknown')}")
            self.logger.info(f"   Android版本: {info.get('version', 'Unknown')}")
            self.logger.info(
                f"   屏幕尺寸: {info.get('displayWidth', 'Unknown')}x{info.get('displayHeight', 'Unknown')}"
            )

        except Exception as e:
            self.logger.error(f"❌ uiautomator2 连接失败: {e}")
            self.logger.error("原因可能是:")
            self.logger.error("1. 未安装 uiautomator2: pip install uiautomator2")
            self.logger.error("2. 未初始化设备: python -m uiautomator2 init")
            self.logger.error("3. 设备权限问题")
            raise e

    def capture_screen(self, save_path=None, step=None, attempt=None):
        """
        截取当前屏幕

        Args:
            save_path: 保存截图的路径，如果为None则自动生成
            step: 步骤编号（从1开始）
            attempt: 尝试编号（从1开始）

        Returns:
            str: 截图文件路径
        """
        try:
            # 如果没有指定保存路径，自动生成
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # 构建文件名，包含step信息
                if step is not None and attempt is not None:
                    filename = f"screenshot_{timestamp}_step={step}_{attempt}.png"
                elif step is not None:
                    filename = f"screenshot_{timestamp}_step={step}_1.png"
                else:
                    filename = f"screenshot_{timestamp}.png"

                if self.current_task_folder:
                    save_path = os.path.join(self.current_task_folder, filename)
                else:
                    save_path = os.path.join(self.screenshots_dir, filename)

            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法截屏")

            # 使用 uiautomator2 截屏
            screenshot = self.u2_device.screenshot()
            screenshot.save(save_path)
            self.logger.debug(f"已使用 uiautomator2 截屏，保存到: {save_path}")

            return save_path

        except Exception as e:
            self.logger.error(f"截屏失败: {e}")
            # 不抛出异常，让程序继续
            return None

    def tap(self, x, y):
        """
        在指定坐标点击

        Args:
            x: X坐标
            y: Y坐标
        """
        try:
            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法点击")

            # 使用 uiautomator2 点击
            self.u2_device.click(x, y)
            self.logger.debug(f"已使用 uiautomator2 点击坐标: ({x}, {y})")

        except Exception as e:
            self.logger.error(f"点击操作失败: {e}")
            # 不抛出异常，让程序继续

    def swipe(self, x1, y1, x2, y2, duration=1000):
        """
        滑动操作

        Args:
            x1, y1: 起始坐标
            x2, y2: 结束坐标
            duration: 滑动持续时间(毫秒)
        """
        try:
            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法滑动")

            # 使用 uiautomator2 滑动 (duration单位为秒)
            duration_sec = duration / 1000.0
            self.u2_device.swipe(x1, y1, x2, y2, duration_sec)
            self.logger.debug(f"已使用 uiautomator2 滑动: ({x1}, {y1}) -> ({x2}, {y2})")

        except Exception as e:
            self.logger.error(f"滑动操作失败: {e}")
            # 不抛出异常，让程序继续

    def input_text(self, text):
        """
        输入文本 - 使用 uiautomator2 支持中文

        Args:
            text: 要输入的文本
        """
        self.logger.debug(f"🔤 准备输入文本: '{text}'")
        self.logger.debug(f"🔍 uiautomator2设备状态: {self.u2_device is not None}")

        try:
            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法输入文本")

            # 使用 uiautomator2 输入（原生支持中文）
            self.logger.debug(f"✅ 使用 uiautomator2 输入中文")
            self.u2_device.send_keys(text)
            self.logger.debug(f"✅ 已使用 uiautomator2 成功输入文本: {text}")

        except Exception as e:
            self.logger.error(f"❌ 文本输入失败: {e}")
            # 不抛出异常，让程序继续

    def press_key(self, keycode):
        """
        按键操作

        Args:
            keycode: 按键码 (如: KEYCODE_BACK=4, KEYCODE_HOME=3, KEYCODE_MENU=82)
        """
        try:
            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法按键")

            # 使用 uiautomator2 按键
            # 将keycode转换为对应的按键名
            key_mapping = {
                3: "home",
                4: "back",
                82: "menu",
                24: "volume_up",
                25: "volume_down",
                26: "power",
                279: "paste",
            }

            if keycode in key_mapping:
                self.u2_device.press(key_mapping[keycode])
                self.logger.debug(f"已使用 uiautomator2 按下按键: {key_mapping[keycode]} ({keycode})")
            else:
                # 使用通用按键事件
                self.u2_device.keyevent(keycode)
                self.logger.debug(f"已使用 uiautomator2 按下按键: {keycode}")

        except Exception as e:
            self.logger.error(f"按键操作失败: {e}")
            # 不抛出异常，让程序继续

    def long_press(self, x, y, duration=2000):
        """
        长按操作

        Args:
            x: X坐标
            y: Y坐标
            duration: 长按持续时间(毫秒)
        """
        try:
            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法长按")

            # 使用 uiautomator2 长按 (duration单位为秒)
            duration_sec = duration / 1000.0
            self.u2_device.long_click(x, y, duration_sec)
            self.logger.debug(f"已使用 uiautomator2 长按坐标: ({x}, {y}), 持续时间: {duration}ms")

        except Exception as e:
            self.logger.error(f"长按操作失败: {e}")
            # 不抛出异常，让程序继续

    def scroll(self, x, y, direction, distance=500):
        """
        滚动操作

        Args:
            x: 滚动中心X坐标
            y: 滚动中心Y坐标
            direction: 滚动方向 ('up', 'down', 'left', 'right')
            distance: 滚动距离(像素)
        """
        try:
            # 计算滚动的起始和结束坐标
            if direction == "up":
                x1, y1 = x, y - distance // 2
                x2, y2 = x, y + distance // 2
            elif direction == "down":
                x1, y1 = x, y + distance // 2
                x2, y2 = x, y - distance // 2
            elif direction == "left":
                x1, y1 = x + distance // 2, y
                x2, y2 = x - distance // 2, y
            elif direction == "right":
                x1, y1 = x - distance // 2, y
                x2, y2 = x + distance // 2, y
            else:
                raise ValueError(f"不支持的滚动方向: {direction}")

            # 使用swipe方法执行滚动（swipe方法已经升级为uiautomator2）
            self.swipe(x1, y1, x2, y2, 500)
            self.logger.debug(f"已滚动: 方向={direction}, 中心=({x}, {y})")

        except Exception as e:
            self.logger.error(f"滚动操作失败: {e}")
            # 不抛出异常，让程序继续

    def open_app(self, app_name):
        """
        打开应用

        Args:
            app_name: 应用名称
        """
        try:
            # 常用应用包名映射
            common_apps = {
                "高德地图": APP_TASKS_MAP[AppEnum.GAODE].package_name,
                "高德": APP_TASKS_MAP[AppEnum.GAODE].package_name,
                "腾讯会议": APP_TASKS_MAP[AppEnum.TENCENT_MEETING].package_name,
                "网易云音乐": APP_TASKS_MAP[AppEnum.MUSIC].package_name,
                "音乐": APP_TASKS_MAP[AppEnum.MUSIC].package_name,
                "B站": APP_TASKS_MAP[AppEnum.BILIBILI].package_name,
                "哔哩哔哩": APP_TASKS_MAP[AppEnum.BILIBILI].package_name,
                "饿了么": APP_TASKS_MAP[AppEnum.ELEME].package_name,
                "小红书": APP_TASKS_MAP[AppEnum.RED_NOTE].package_name,
                "携程旅行": APP_TASKS_MAP[AppEnum.CTRIP].package_name,
                "携程": APP_TASKS_MAP[AppEnum.CTRIP].package_name,
                "微信": APP_TASKS_MAP[AppEnum.WECHAT].package_name,
            }

            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法打开应用")

            # 使用 uiautomator2 启动应用
            if app_name in common_apps:
                package_name = common_apps[app_name]
                self.u2_device.app_start(package_name)
                self.logger.debug(f"已使用 uiautomator2 打开应用: {app_name} ({package_name})")
            else:
                # 尝试直接使用app_name作为包名
                try:
                    self.u2_device.app_start(app_name)
                    self.logger.debug(f"已使用 uiautomator2 打开应用: {app_name}")
                except:
                    self.logger.warning(f"无法直接启动应用 {app_name}，可能需要完整包名")

        except Exception as e:
            self.logger.error(f"打开应用失败: {e}")
            # 不抛出异常，让程序继续

    def drag(self, x1, y1, x2, y2, duration=1000):
        """
        拖拽操作（与swipe相同，但语义不同）

        Args:
            x1, y1: 起始坐标
            x2, y2: 结束坐标
            duration: 拖拽持续时间(毫秒)
        """
        # 直接调用swipe方法（已经升级为uiautomator2）
        self.swipe(x1, y1, x2, y2, duration)
        self.logger.debug(f"已拖拽: ({x1}, {y1}) -> ({x2}, {y2})")

    def press_home(self):
        """返回主屏幕"""
        self.press_key(3)  # KEYCODE_HOME = 3
        self.logger.debug("已返回主屏幕")

    def press_back(self):
        """返回上一页"""
        self.press_key(4)  # KEYCODE_BACK = 4
        self.logger.debug("已返回上一页")

    def encode_image(self, image_path):
        """将图片转换为base64编码"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def get_ai_action(self, instruction, language="English", image_path=None):
        """
        获取AI分析结果和操作建议

        Args:
            instruction: 操作指令
            language: 语言
            image_path: 图片路径，如果为None则自动截屏

        Returns:
            str: AI返回的操作建议
        """
        # 如果没有提供图片路径，则自动截屏
        if image_path is None:
            image_path = self.capture_screen()

        # 构造系统提示
        system_prompt = PHONE_USE_DOUBAO.format(instruction=instruction, language=language)

        # 编码图片
        image_format = image_path.split(".")[-1]
        base64_image = self.encode_image(image_path)

        # 构造消息
        messages = [{"role": "user", "content": system_prompt}]

        # 添加历史对话
        messages.extend(self.conversation_messages)

        # 添加当前图片
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/{image_format};base64,{base64_image}"},
                    }
                ],
            }
        )

        # 调用AI API
        response = self.client.chat.completions.create(model=self.model_name, messages=messages, **self.model_kwargs)

        # 获取完整响应
        full_response = response.choices[0].message.content

        # 保存到历史
        self.conversation_messages.append({"role": "assistant", "content": full_response})

        # 保持最多8条消息（4轮对话）
        if len(self.conversation_messages) > 8:
            self.conversation_messages = self.conversation_messages[2:]

        return full_response

    def parse_coordinates(self, point_str):
        """
        从point字符串中解析坐标

        Args:
            point_str: 包含坐标的字符串，格式如 '<point>x y</point>'

        Returns:
            tuple: (x, y) 坐标，如果解析失败返回None
        """
        # 获取屏幕尺寸
        screen_size = self.get_screen_size()
        if not screen_size:
            return None

        width, height = screen_size

        # 解析坐标
        match = re.search(r"<point>(\d+)\s+(\d+)</point>", point_str)
        if match:
            # 将千分比坐标转换为绝对坐标
            x = int(int(match.group(1)) / 1000 * width)
            y = int(int(match.group(2)) / 1000 * height)
            return (x, y)

        return None

    def parse_ai_actions(self, ai_response):
        """
        解析AI响应中的所有动作

        Args:
            ai_response: AI的响应文本

        Returns:
            list: 动作列表，每个动作是一个字典
        """
        # 使用新的解析器
        return self.action_parser.parse_ai_response(ai_response)

    def execute_action(self, action):
        """
        执行单个动作

        Args:
            action: 动作字典，包含action类型和相关参数

        Returns:
            bool: 执行是否成功
        """
        try:
            action_type = action.get("action")

            if action_type == "click":
                point = action.get("point")
                coordinates = self.parse_coordinates(point)
                if coordinates:
                    self.tap(*coordinates)
                    return True
                else:
                    self.logger.warning(f"无法解析点击坐标: {point}")
                    return False

            elif action_type == "long_press":
                point = action.get("point")
                coordinates = self.parse_coordinates(point)
                if coordinates:
                    self.long_press(*coordinates)
                    return True
                else:
                    self.logger.warning(f"无法解析长按坐标: {point}")
                    return False

            elif action_type == "type":
                content = action.get("content", "")
                # 处理换行符
                content = content.replace("\\n", "\n")
                self.input_text(content)
                return True

            elif action_type == "scroll":
                point = action.get("point")
                direction = action.get("direction", "down")
                coordinates = self.parse_coordinates(point)
                if coordinates:
                    self.scroll(*coordinates, direction)
                    return True
                else:
                    self.logger.warning(f"无法解析滚动坐标: {point}")
                    return False

            elif action_type == "open_app":
                app_name = action.get("app_name", "")
                self.open_app(app_name)
                return True

            elif action_type == "drag":
                start_point = action.get("start_point")
                end_point = action.get("end_point")
                start_coords = self.parse_coordinates(start_point)
                end_coords = self.parse_coordinates(end_point)
                if start_coords and end_coords:
                    self.drag(*start_coords, *end_coords)
                    return True
                else:
                    self.logger.warning(f"无法解析拖拽坐标: {start_point} -> {end_point}")
                    return False

            elif action_type == "press_home":
                self.press_home()
                return True

            elif action_type == "press_back":
                self.press_back()
                return True

            elif action_type == "finished":
                content = action.get("content", "操作完成")
                self.logger.info(f"任务完成: {content}")
                return True

            else:
                self.logger.warning(f"不支持的动作类型: {action_type}")
                return False

        except Exception as e:
            self.logger.error(f"执行动作失败: {e}")
            return False

    def get_screen_size(self):
        """
        获取屏幕尺寸

        Returns:
            tuple: (width, height) 或 None
        """
        try:
            if not self.u2_device:
                raise RuntimeError("uiautomator2 设备未连接，无法获取屏幕尺寸")

            # 使用 uiautomator2 获取屏幕尺寸
            width, height = self.u2_device.window_size()
            self.logger.debug(f"已使用 uiautomator2 获取屏幕尺寸: {width}x{height}")
            return (width, height)

        except Exception as e:
            self.logger.error(f"获取屏幕尺寸失败: {e}")

        return None
