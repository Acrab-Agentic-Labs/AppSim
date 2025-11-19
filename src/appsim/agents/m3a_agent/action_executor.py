# -*- coding: utf-8 -*-
"""Action Executor - 将 JSON Action 转换为 uiautomator2 操作"""

import logging
import time
from typing import Any, Dict, Optional

import uiautomator2 as u2


class ActionExecutor:
    """动作执行器，将 M3A 的 JSON Action 转换为 uiautomator2 操作"""

    def __init__(self, u2_device: u2.Device):
        """初始化动作执行器.

        Args:
            u2_device: uiautomator2 设备对象
        """
        self.u2_device = u2_device

    def execute_action(self, action: Dict[str, Any], ui_elements: list) -> bool:
        """执行动作.

        Args:
            action: JSON 格式的动作字典
            ui_elements: UI 元素列表，用于通过 index 获取坐标

        Returns:
            bool: 是否执行成功
        """
        try:
            if not isinstance(action, dict):
                logging.error(f"错误: action 不是字典类型，而是 {type(action)}: {action}")
                return False

            action_type = action.get("action_type")
            if not action_type:
                logging.error(f"错误: action 缺少 'action_type' 字段: {action}")
                return False

            if action_type == "click":
                return self._execute_click(action, ui_elements)
            elif action_type == "long_press":
                return self._execute_long_press(action, ui_elements)
            elif action_type == "input_text":
                return self._execute_input_text(action, ui_elements)
            elif action_type == "scroll":
                return self._execute_scroll(action, ui_elements)
            elif action_type == "keyboard_enter":
                return self._execute_keyboard_enter()
            elif action_type == "navigate_home":
                return self._execute_navigate_home()
            elif action_type == "navigate_back":
                return self._execute_navigate_back()
            elif action_type == "open_app":
                return self._execute_open_app(action)
            elif action_type == "wait":
                return self._execute_wait()
            elif action_type == "status":
                # status 动作不需要执行，只是标记任务完成
                return True
            elif action_type == "answer":
                # answer 动作不需要执行，只是回答用户问题
                return True
            else:
                logging.error(f"未知的动作类型: {action_type}")
                return False

        except Exception as e:
            logging.error(f"执行动作时出错: {e}")
            return False

    def _get_element_center(self, index: int, ui_elements: list) -> Optional[tuple]:
        """通过 index 获取元素的中心坐标.

        Args:
            index: UI 元素索引
            ui_elements: UI 元素列表

        Returns:
            tuple: (x, y) 坐标，如果失败则返回 None
        """
        if index is None or index >= len(ui_elements):
            return None

        ui_element = ui_elements[index]
        left, top, right, bottom = ui_element.bounds
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        return (center_x, center_y)

    def _execute_click(self, action: Dict[str, Any], ui_elements: list) -> bool:
        """执行点击动作"""
        index = action.get("index")
        if index is None:
            logging.error("click 动作缺少 index 参数")
            return False

        center = self._get_element_center(index, ui_elements)
        if center is None:
            logging.error(f"无法获取元素 {index} 的坐标")
            return False

        x, y = center
        self.u2_device.click(x, y)
        logging.debug(f"点击坐标: ({x}, {y})")
        return True

    def _execute_long_press(self, action: Dict[str, Any], ui_elements: list) -> bool:
        """执行长按动作"""
        index = action.get("index")
        if index is None:
            logging.error("long_press 动作缺少 index 参数")
            return False

        center = self._get_element_center(index, ui_elements)
        if center is None:
            logging.error(f"无法获取元素 {index} 的坐标")
            return False

        x, y = center
        self.u2_device.long_click(x, y, duration=1.0)
        logging.debug(f"长按坐标: ({x}, {y})")
        return True

    def _execute_input_text(self, action: Dict[str, Any], ui_elements: list) -> bool:
        """执行输入文本动作"""
        index = action.get("index")
        text = action.get("text")

        if text is None:
            logging.error("input_text 动作缺少 text 参数")
            return False

        # 如果指定了 index，先点击该元素
        if index is not None:
            center = self._get_element_center(index, ui_elements)
            if center:
                x, y = center
                self.u2_device.click(x, y)
                time.sleep(0.5)  # 等待输入框获得焦点

        # 输入文本
        self.u2_device.send_keys(text)
        logging.debug(f"输入文本: {text}")

        # 按回车
        self.u2_device.press("enter")
        return True

    def _execute_scroll(self, action: Dict[str, Any], ui_elements: list) -> bool:
        """执行滚动动作"""
        direction = action.get("direction")
        index = action.get("index")

        if direction is None:
            logging.error("scroll 动作缺少 direction 参数")
            return False

        # 获取屏幕尺寸
        info = self.u2_device.info
        screen_width = info.get("displayWidth", 1080)
        screen_height = info.get("displayHeight", 1920)

        # 确定滚动起点和终点
        if index is not None:
            # 滚动特定元素
            center = self._get_element_center(index, ui_elements)
            if center is None:
                logging.error(f"无法获取元素 {index} 的坐标")
                return False
            start_x, start_y = center
        else:
            # 滚动整个屏幕
            start_x = screen_width // 2
            start_y = screen_height // 2

        # 根据方向确定终点
        scroll_distance = min(screen_width, screen_height) // 3

        if direction == "up":
            end_x, end_y = start_x, start_y + scroll_distance
        elif direction == "down":
            end_x, end_y = start_x, start_y - scroll_distance
        elif direction == "left":
            end_x, end_y = start_x + scroll_distance, start_y
        elif direction == "right":
            end_x, end_y = start_x - scroll_distance, start_y
        else:
            logging.error(f"未知的滚动方向: {direction}")
            return False

        # 执行滑动
        self.u2_device.swipe(start_x, start_y, end_x, end_y, duration=0.5)
        logging.debug(f"滚动方向: {direction}, 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
        return True

    def _execute_keyboard_enter(self) -> bool:
        """执行键盘回车"""
        self.u2_device.press("enter")
        logging.debug("按下回车键")
        return True

    def _execute_navigate_home(self) -> bool:
        """导航到主屏幕"""
        self.u2_device.press("home")
        logging.debug("返回主屏幕")
        return True

    def _execute_navigate_back(self) -> bool:
        """导航返回"""
        self.u2_device.press("back")
        logging.debug("返回上一页")
        return True

    def _execute_open_app(self, action: Dict[str, Any]) -> bool:
        """打开应用"""
        app_name = action.get("app_name")
        if app_name is None:
            logging.error("open_app 动作缺少 app_name 参数")
            return False

        try:
            # 尝试通过包名打开
            self.u2_device.app_start(app_name)
            logging.debug(f"打开应用: {app_name}")
            return True
        except:
            # 如果失败，尝试通过名称查找
            try:
                # 获取所有应用
                apps = self.u2_device.app_list()
                # 尝试模糊匹配
                for app in apps:
                    if app_name.lower() in app.lower() or app.lower() in app_name.lower():
                        self.u2_device.app_start(app)
                        logging.debug(f"打开应用: {app} (匹配 {app_name})")
                        return True
                logging.error(f"未找到应用: {app_name}")
                return False
            except Exception as e:
                logging.error(f"打开应用失败: {e}")
                return False

    def _execute_wait(self) -> bool:
        """等待"""
        time.sleep(1.0)
        logging.debug("等待 1 秒")
        return True
