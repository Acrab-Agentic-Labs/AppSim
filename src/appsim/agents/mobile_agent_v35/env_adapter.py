# -*- coding: utf-8 -*-
"""Mobile-Agent-v3.5 到 AppSim/uiautomator2 的环境适配器。"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import uiautomator2 as u2

logger = logging.getLogger(__name__)

OFFICIAL_SCREEN_WIDTH = 1080
OFFICIAL_SCREEN_HEIGHT = 2400


@dataclass
class MobileAgentAppSimState:
    """满足官方 Mobile-Agent 所需字段的最小环境状态。"""

    pixels: np.ndarray
    forest: Any = None
    ui_elements: List[Any] = field(default_factory=list)
    auxiliaries: Dict[str, Any] = field(default_factory=dict)


class MobileAgentAppSimEnvAdapter:
    """使用 uiautomator2 为官方 Mobile-Agent-v3.5 提供环境接口。"""

    def __init__(
        self,
        device_id: str,
        app_package: str,
        action_module: Any,
        wait_seconds: float = 1.0,
        stabilize_seconds: float = 0.5,
        action_settle_seconds: float = 2.0,
    ) -> None:
        if not device_id:
            raise ValueError("device_id 不能为空")
        if not app_package:
            raise ValueError("app_package 不能为空")

        self.device_id = device_id
        self.app_package = app_package
        self.action_module = action_module
        self.wait_seconds = max(0.0, wait_seconds)
        self.stabilize_seconds = max(0.0, stabilize_seconds)
        self.action_settle_seconds = max(0.0, action_settle_seconds)
        self.u2_device = u2.connect(device_id)

        self._interaction_cache = ""
        self._closed = False
        self._last_pixels: Optional[np.ndarray] = None
        self._last_screen_size = self._read_screen_size()
        self.last_error: Optional[str] = None
        self.action_errors: List[Dict[str, str]] = []
        self.questions: List[str] = []

    @property
    def controller(self) -> u2.Device:
        """兼容 AndroidWorld 接口；控制器即当前 uiautomator2 设备。"""
        return self.u2_device

    @property
    def interaction_cache(self) -> str:
        return self._interaction_cache

    @interaction_cache.setter
    def interaction_cache(self, value: str) -> None:
        self._interaction_cache = value or ""

    def _record_error(self, operation: str, error: Exception) -> None:
        message = f"{operation}: {error}"
        self.last_error = message
        self.action_errors.append(
            {
                "operation": operation,
                "error": str(error),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        logger.error("Mobile-Agent AppSim 环境操作失败: %s", message)

    def _read_screen_size(self) -> Tuple[int, int]:
        try:
            info = self.u2_device.info
            width = int(info.get("displayWidth", OFFICIAL_SCREEN_WIDTH))
            height = int(info.get("displayHeight", OFFICIAL_SCREEN_HEIGHT))
            if width <= 0 or height <= 0:
                raise ValueError(f"无效屏幕尺寸: {width}x{height}")
            return width, height
        except Exception as error:
            if hasattr(self, "action_errors"):
                self._record_error("读取屏幕尺寸", error)
            return getattr(
                self,
                "_last_screen_size",
                (OFFICIAL_SCREEN_WIDTH, OFFICIAL_SCREEN_HEIGHT),
            )

    def _scale_point(self, x: Any, y: Any) -> Tuple[int, int]:
        """将官方 1080x2400 坐标反向映射到实际设备分辨率。"""
        width, height = self.logical_screen_size
        scaled_x = round(float(x) * width / OFFICIAL_SCREEN_WIDTH)
        scaled_y = round(float(y) * height / OFFICIAL_SCREEN_HEIGHT)
        return (
            min(max(scaled_x, 0), width - 1),
            min(max(scaled_y, 0), height - 1),
        )

    def _blank_pixels(self) -> np.ndarray:
        width, height = self.logical_screen_size
        return np.zeros((height, width, 3), dtype=np.uint8)

    def reset(self, go_home: bool = False) -> MobileAgentAppSimState:
        """清理环境侧状态；App 的数据清理由 AppSim 评测器负责。"""
        self._interaction_cache = ""
        self.last_error = None
        self.action_errors = []
        self.questions = []
        if go_home:
            try:
                self.u2_device.press("home")
            except Exception as error:
                self._record_error("返回桌面", error)
        return self.get_state(wait_to_stabilize=False)

    def get_state(self, wait_to_stabilize: bool = False) -> MobileAgentAppSimState:
        """读取 RGB 截图；失败时返回上一帧，避免中断官方 step。"""
        if wait_to_stabilize and self.stabilize_seconds:
            time.sleep(self.stabilize_seconds)

        try:
            screenshot = self.u2_device.screenshot()
            if hasattr(screenshot, "convert"):
                pixels = np.asarray(screenshot.convert("RGB"), dtype=np.uint8)
            else:
                pixels = np.asarray(screenshot, dtype=np.uint8)
            if pixels.ndim != 3 or pixels.shape[2] < 3:
                raise ValueError(f"无效截图形状: {pixels.shape}")
            pixels = pixels[:, :, :3].copy()
            self._last_pixels = pixels
        except Exception as error:
            self._record_error("获取截图", error)
            raise RuntimeError("获取设备截图失败") from error

        return MobileAgentAppSimState(
            pixels=pixels,
            auxiliaries={"last_error": self.last_error},
        )

    def execute_action(self, action: Any) -> None:
        """执行官方 JSONAction；异常记录后交回官方 step 处理。"""
        try:
            json_action = self.action_module
            action_type = action.action_type
            if action_type == json_action.CLICK:
                x, y = self._scale_point(action.x, action.y)
                self.u2_device.click(x, y)
            elif action_type == json_action.LONG_PRESS:
                x, y = self._scale_point(action.x, action.y)
                self.u2_device.long_click(x, y, duration=1.0)
            elif action_type in (json_action.INPUT_TEXT, json_action.TYPE):
                self.u2_device.set_fastinput_ime()
                self.u2_device.send_keys(action.text or "")
                self.u2_device.press("enter")
            elif action_type == json_action.SWIPE:
                if not isinstance(action.direction, (list, tuple)) or len(action.direction) != 4:
                    raise ValueError(f"无效 swipe 坐标: {action.direction}")
                x1, y1 = self._scale_point(action.direction[0], action.direction[1])
                x2, y2 = self._scale_point(action.direction[2], action.direction[3])
                self.u2_device.swipe(x1, y1, x2, y2, duration=0.5)
            elif action_type == json_action.KEYBOARD_ENTER:
                self.u2_device.press("enter")
            elif action_type == json_action.NAVIGATE_BACK:
                self.u2_device.press("back")
            elif action_type == json_action.NAVIGATE_HOME:
                self.u2_device.press("home")
            elif action_type == json_action.SYSTEM_BUTTON:
                self._execute_system_button(action)
            elif action_type in (json_action.OPEN_APP, json_action.OPEN):
                # AppSim 每条任务只允许重新打开当前评测 App。
                self.u2_device.app_start(self.app_package)
            elif action_type == json_action.WAIT:
                time.sleep(self.wait_seconds)
            elif action_type == json_action.ANSWER:
                self._interaction_cache = action.text or ""
            elif action_type in (json_action.STATUS, json_action.TERMINATE):
                return
            else:
                raise ValueError(f"不支持的动作类型: {action_type}")
            if self.action_settle_seconds:
                time.sleep(self.action_settle_seconds)
        except Exception as error:
            self._record_error(repr(action), error)
            raise

    def _execute_system_button(self, action: Any) -> None:
        button = (action.keycode or action.text or "").lower()
        mapping = {
            "keycode_back": "back",
            "back": "back",
            "keycode_home": "home",
            "home": "home",
            "keycode_enter": "enter",
            "enter": "enter",
        }
        if button not in mapping:
            raise ValueError(f"不支持的系统按键: {button}")
        self.u2_device.press(mapping[button])

    @property
    def foreground_activity_name(self) -> str:
        try:
            current = self.u2_device.app_current()
            package = current.get("package", "")
            activity = current.get("activity", "")
            return f"{package}/{activity}" if activity else package
        except Exception as error:
            self._record_error("读取前台 Activity", error)
            return ""

    @property
    def device_screen_size(self) -> Tuple[int, int]:
        self._last_screen_size = self._read_screen_size()
        return self._last_screen_size

    @property
    def logical_screen_size(self) -> Tuple[int, int]:
        return self.device_screen_size

    @property
    def orientation(self) -> int:
        try:
            return int(self.u2_device.info.get("displayRotation", 0))
        except Exception as error:
            self._record_error("读取屏幕方向", error)
            return 0

    @property
    def physical_frame_boundary(self) -> Tuple[int, int, int, int]:
        width, height = self.logical_screen_size
        return 0, 0, width, height

    def hide_automation_ui(self) -> None:
        try:
            self.u2_device.shell("settings put system pointer_location 0")
        except Exception as error:
            self._record_error("隐藏坐标指示器", error)

    def ask_question(self, question: str, timeout_seconds: float = -1.0) -> None:
        """评测期间禁止等待人工输入，仅记录问题。"""
        del timeout_seconds
        self.questions.append(question)
        logger.warning("Mobile-Agent 在评测期间请求人工回答: %s", question)
        return None

    def close(self) -> None:
        """uiautomator2 无需显式断开连接。"""
        self._closed = True
        self._interaction_cache = ""
