# -*- coding: utf-8 -*-
"""uiautomator2 Environment Wrapper for M3A Agent"""

import logging
import time
import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple

import numpy as np
import uiautomator2 as u2

logger = logging.getLogger(__name__)


class UIElement:
    """UI 元素数据结构，兼容 M3A 的 UIElement 接口"""

    def __init__(
            self,
            bounds: Tuple[int, int, int, int],  # (left, top, right, bottom)
            text: Optional[str] = None,
            content_description: Optional[str] = None,
            hint_text: Optional[str] = None,
            tooltip: Optional[str] = None,
            is_clickable: bool = False,
            is_long_clickable: bool = False,
            is_editable: bool = False,
            is_scrollable: bool = False,
            is_focusable: bool = False,
            is_selected: bool = False,
            is_checked: bool = False,
            class_name: Optional[str] = None,
            resource_name: Optional[str] = None,
            package_name: Optional[str] = None,
    ):
        self.bounds = bounds
        self.text = text
        self.content_description = content_description
        self.hint_text = hint_text
        self.tooltip = tooltip
        self.is_clickable = is_clickable
        self.is_long_clickable = is_long_clickable
        self.is_editable = is_editable
        self.is_scrollable = is_scrollable
        self.is_focusable = is_focusable
        self.is_selected = is_selected
        self.is_checked = is_checked
        self.class_name = class_name
        self.resource_name = resource_name
        self.package_name = package_name


class U2Env:
    """uiautomator2 环境封装，提供类似 android_world env 的接口"""

    def __init__(self, device_id: str):
        """初始化 uiautomator2 环境.

        Args:
            device_id: 设备 ID（必需参数）
        """
        if not device_id:
            raise ValueError("device_id is required")

        self.device_id = device_id
        self.u2_device = None
        self._check_and_connect()

    def _check_and_connect(self):
        """检查并连接设备"""
        try:
            # 连接 uiautomator2
            self.u2_device = u2.connect(self.device_id)
            info = self.u2_device.info
            logger.info("✅ uiautomator2 连接成功!")
            logger.info(f"   设备: {self.device_id}")
            logger.info(f"   屏幕尺寸: {info.get('displayWidth', 'Unknown')}x{info.get('displayHeight', 'Unknown')}")

        except Exception as e:
            logger.error(f"uiautomator2 连接失败: {e}")
            raise RuntimeError(f"uiautomator2 连接失败: {e}")

    def reset(self, go_home: bool = False):
        """重置环境.

        Args:
            go_home: 是否返回主屏幕
        """
        if go_home:
            self.u2_device.press("home")
            time.sleep(1)

    def get_state(self, wait_to_stabilize: bool = True) -> dict:
        """获取当前状态.

        Args:
            wait_to_stabilize: 是否等待界面稳定

        Returns:
            dict: 包含 pixels (numpy array) 和 ui_elements (list) 的状态字典
        """
        if wait_to_stabilize:
            time.sleep(0.5)

        # 获取截图
        screenshot = self.u2_device.screenshot()
        pixels = np.array(screenshot)

        # 获取 UI 元素
        ui_elements = self._get_ui_elements()

        return {
            "pixels": pixels,
            "ui_elements": ui_elements,
        }

    def _get_ui_elements(self) -> List[UIElement]:
        """从 uiautomator2 获取 UI 元素列表，通过解析 dump_hierarchy XML
        优先包含可交互的控件，同时保留有文本或 content-desc 的元素
        """
        ui_elements = []
        interactive_elements = []  # 可交互元素
        other_elements = []  # 其他有用元素

        try:
            # 获取 UI hierarchy XML
            xml_str = self.u2_device.dump_hierarchy(compressed=False, pretty=False)

            if not xml_str:
                logger.warning("警告: dump_hierarchy 返回空字符串")
                return ui_elements

            # 解析 XML
            try:
                root = ET.fromstring(xml_str)
            except ET.ParseError as e:
                logger.error(f"XML 解析失败: {e}")
                return ui_elements

            # 递归遍历所有 node 元素
            def parse_node(node: ET.Element):
                """解析单个 node 元素"""
                # 获取 bounds 属性，格式通常是 "[left,top][right,bottom]"
                bounds_str = node.get("bounds", "")
                if not bounds_str:
                    return None

                # 解析 bounds: "[left,top][right,bottom]"
                try:
                    # 移除方括号并分割
                    parts = bounds_str.replace("[", "").replace("]", ",").split(",")
                    if len(parts) >= 4:
                        left = int(parts[0])
                        top = int(parts[1])
                        right = int(parts[2])
                        bottom = int(parts[3])
                    else:
                        return None

                    # 检查边界是否有效
                    if right <= left or bottom <= top:
                        return None
                except (ValueError, IndexError):
                    return None

                # 解析布尔属性
                def parse_bool(attr: str, default: bool = False) -> bool:
                    value = node.get(attr, "").lower()
                    return value == "true" if value else default

                # 获取属性值
                is_clickable = parse_bool("clickable", False)
                is_long_clickable = parse_bool("long-clickable", False)
                is_editable = parse_bool("editable", False)
                is_scrollable = parse_bool("scrollable", False)
                is_focusable = parse_bool("focusable", False)
                text = node.get("text") or None
                content_desc = node.get("content-desc") or None
                hint_text = node.get("hint") or None
                class_name = node.get("class") or None
                resource_name = node.get("resource-id") or None
                package_name = node.get("package") or None

                # 判断是否为可交互元素
                is_interactive = is_clickable or is_long_clickable or is_editable or is_scrollable or is_focusable

                # 判断是否为有用元素（有文本、content-desc 或可交互）
                is_useful = is_interactive or text or content_desc or hint_text

                if not is_useful:
                    return None

                # 创建 UIElement
                ui_element = UIElement(
                    bounds=(left, top, right, bottom),
                    text=text,
                    content_description=content_desc,
                    hint_text=hint_text,
                    tooltip=None,  # Android UI hierarchy 通常没有 tooltip
                    is_clickable=is_clickable,
                    is_long_clickable=is_long_clickable,
                    is_editable=is_editable,
                    is_scrollable=is_scrollable,
                    is_focusable=is_focusable,
                    is_selected=parse_bool("selected", False),
                    is_checked=parse_bool("checked", False),
                    class_name=class_name,
                    resource_name=resource_name,
                    package_name=package_name,
                )

                return ui_element, is_interactive

            # 遍历所有 node 元素
            for node in root.iter("node"):
                result = parse_node(node)
                if result:
                    ui_element, is_interactive = result
                    if is_interactive:
                        interactive_elements.append(ui_element)
                    else:
                        other_elements.append(ui_element)

            # 优先添加可交互元素，然后添加其他有用元素
            ui_elements = interactive_elements + other_elements

        except Exception as e:
            logger.error(f"获取 UI 元素时出错: {e}", exc_info=True)

        return ui_elements

    @property
    def logical_screen_size(self) -> Tuple[int, int]:
        """获取逻辑屏幕尺寸（像素）"""
        info = self.u2_device.info
        return (info.get("displayWidth", 1080), info.get("displayHeight", 1920))

    @property
    def orientation(self) -> int:
        """获取屏幕方向（0=竖屏, 1=横屏）"""
        info = self.u2_device.info
        return info.get("displayRotation", 0)

    @property
    def physical_frame_boundary(self) -> Tuple[int, int, int, int]:
        """获取物理帧边界"""
        width, height = self.logical_screen_size
        return (0, 0, width, height)

    def hide_automation_ui(self):
        """隐藏自动化 UI（在 uiautomator2 中不需要）"""
        pass

    def close(self):
        """关闭环境"""
        # uiautomator2 不需要显式关闭
        pass