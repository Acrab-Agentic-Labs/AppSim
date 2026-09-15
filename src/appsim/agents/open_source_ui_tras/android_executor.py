# -*- coding: utf-8 -*-
"""将 UI-TARS 官方结构化动作转换为 Android 操作。"""

import ast
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Sequence, Tuple


@dataclass(frozen=True)
class ActionOutcome:
    """单个 Android 动作的执行结果。"""

    success: bool
    should_stop: bool = False
    task_success: bool = False
    final_message: Optional[str] = None


class AndroidActionExecutor:
    """使用 uiautomator2 执行官方 UI-TARS 动作。"""

    def __init__(self, device: Any):
        self.device = device

    def execute(self, action: Dict[str, Any]) -> ActionOutcome:
        action_type = str(action.get("action_type") or "").strip().lower()
        action_inputs = action.get("action_inputs") or {}

        if action_type in {"finished", "answer"}:
            final_message = self._first_text(
                action_inputs,
                "content",
                "text",
                "answer",
            )
            return ActionOutcome(
                success=True,
                should_stop=True,
                task_success=True,
                final_message=final_message or action.get("thought") or "任务已完成",
            )

        if action_type == "call_user":
            final_message = self._first_text(
                action_inputs,
                "content",
                "text",
                "reason",
            )
            return ActionOutcome(
                success=True,
                should_stop=True,
                task_success=False,
                final_message=final_message or "模型请求用户介入",
            )

        if action_type in {"click", "left_single", "right_single"}:
            x, y = self._point_from_inputs(action_inputs)
            self.device.click(x, y)
            return ActionOutcome(success=True)

        if action_type == "left_double":
            x, y = self._point_from_inputs(action_inputs)
            self.device.click(x, y)
            time.sleep(0.1)
            self.device.click(x, y)
            return ActionOutcome(success=True)

        if action_type == "long_press":
            x, y = self._point_from_inputs(action_inputs)
            duration = self._float_value(action_inputs.get("duration"), 1.0)
            self.device.long_click(x, y, duration=max(0.1, duration))
            return ActionOutcome(success=True)

        if action_type in {"drag", "select"}:
            start_x, start_y = self._point_from_inputs(action_inputs)
            end_x, end_y = self._point_from_inputs(
                action_inputs,
                keys=("end_box", "end_point", "coordinate2"),
            )
            duration = self._float_value(action_inputs.get("duration"), 1.0)
            self.device.swipe(
                start_x,
                start_y,
                end_x,
                end_y,
                duration=max(0.1, duration),
            )
            return ActionOutcome(success=True)

        if action_type == "scroll":
            self._scroll(action_inputs)
            return ActionOutcome(success=True)

        if action_type == "type":
            self._type_text(str(action_inputs.get("content") or ""))
            return ActionOutcome(success=True)

        if action_type == "open_app":
            self._open_app(str(action_inputs.get("app_name") or "").strip())
            return ActionOutcome(success=True)

        if action_type == "press_home":
            self.device.press("home")
            return ActionOutcome(success=True)

        if action_type == "press_back":
            self.device.press("back")
            return ActionOutcome(success=True)

        if action_type in {"press", "keydown"}:
            key = self._first_text(action_inputs, "key", "press")
            if not key:
                raise ValueError(f"{action_type} 动作缺少 key 参数")
            self.device.press(self._normalize_key(key))
            return ActionOutcome(success=True)

        if action_type == "wait":
            seconds = self._float_value(
                action_inputs.get("time", action_inputs.get("seconds")),
                5.0,
            )
            time.sleep(min(max(seconds, 0.0), 30.0))
            return ActionOutcome(success=True)

        raise ValueError(f"不支持的 OpenSource-UI-TRAS 动作: {action_type or '<empty>'}")

    def _screen_size(self) -> Tuple[int, int]:
        info = self.device.info
        width = int(info.get("displayWidth", 1080))
        height = int(info.get("displayHeight", 1920))
        if width <= 0 or height <= 0:
            raise ValueError(f"无效的屏幕尺寸: {width}x{height}")
        return width, height

    def _point_from_inputs(
        self,
        action_inputs: Dict[str, Any],
        keys: Sequence[str] = ("start_box", "point", "coordinate"),
    ) -> Tuple[int, int]:
        for key in keys:
            value = action_inputs.get(key)
            if value is not None and value != "":
                return self._normalized_box_center(value)
        raise ValueError(f"动作缺少坐标参数: {', '.join(keys)}")

    def _normalized_box_center(self, value: Any) -> Tuple[int, int]:
        coordinates = self._parse_coordinates(value)
        if len(coordinates) == 2:
            normalized_x, normalized_y = coordinates
        elif len(coordinates) == 4:
            normalized_x = (coordinates[0] + coordinates[2]) / 2
            normalized_y = (coordinates[1] + coordinates[3]) / 2
        else:
            raise ValueError(f"坐标必须包含 2 或 4 个数字: {coordinates}")

        width, height = self._screen_size()
        x = min(width - 1, max(0, round(normalized_x * width)))
        y = min(height - 1, max(0, round(normalized_y * height)))
        return x, y

    @staticmethod
    def _parse_coordinates(value: Any) -> Tuple[float, ...]:
        parsed_value = ast.literal_eval(value) if isinstance(value, str) else value
        if not isinstance(parsed_value, (list, tuple)):
            raise ValueError(f"坐标不是列表或元组: {parsed_value!r}")
        if any(isinstance(item, bool) or not isinstance(item, (int, float)) for item in parsed_value):
            raise ValueError(f"坐标包含非数字内容: {parsed_value!r}")
        return tuple(float(item) for item in parsed_value)

    def _scroll(self, action_inputs: Dict[str, Any]) -> None:
        width, height = self._screen_size()
        try:
            anchor_x, anchor_y = self._point_from_inputs(action_inputs)
        except ValueError:
            anchor_x, anchor_y = width // 2, height // 2

        direction = str(action_inputs.get("direction") or "").strip().lower()
        vertical_distance = max(1, height // 4)
        horizontal_distance = max(1, width // 4)

        if direction == "down":
            start = (anchor_x, min(height - 1, anchor_y + vertical_distance))
            end = (anchor_x, max(0, anchor_y - vertical_distance))
        elif direction == "up":
            start = (anchor_x, max(0, anchor_y - vertical_distance))
            end = (anchor_x, min(height - 1, anchor_y + vertical_distance))
        elif direction == "right":
            start = (min(width - 1, anchor_x + horizontal_distance), anchor_y)
            end = (max(0, anchor_x - horizontal_distance), anchor_y)
        elif direction == "left":
            start = (max(0, anchor_x - horizontal_distance), anchor_y)
            end = (min(width - 1, anchor_x + horizontal_distance), anchor_y)
        else:
            raise ValueError(f"不支持的滚动方向: {direction or '<empty>'}")

        self.device.swipe(*start, *end, duration=0.5)

    def _type_text(self, content: str) -> None:
        should_submit = False
        if content.endswith("\\n"):
            content = content[:-2]
            should_submit = True
        elif content.endswith("\n"):
            content = content[:-1]
            should_submit = True

        self.device.set_fastinput_ime()
        if content:
            self.device.send_keys(content)
        if should_submit:
            self.device.press("enter")

    def _open_app(self, app_name: str) -> None:
        if not app_name:
            raise ValueError("open_app 动作缺少 app_name 参数")
        if "." in app_name:
            self.device.app_start(app_name)
            return

        self.device.press("home")
        time.sleep(1.0)
        selector = self.device(text=app_name)
        if not selector.exists:
            selector = self.device(textContains=app_name)
        if not selector.exists:
            raise ValueError(f"桌面上未找到应用: {app_name}")
        selector.click()

    @staticmethod
    def _first_text(action_inputs: Dict[str, Any], *keys: str) -> Optional[str]:
        for key in keys:
            value = action_inputs.get(key)
            if value is not None and str(value).strip():
                return str(value)
        return None

    @staticmethod
    def _float_value(value: Any, default: float) -> float:
        if value in (None, ""):
            return default
        try:
            return float(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"无法解析数值参数: {value!r}") from error

    @staticmethod
    def _normalize_key(key: str) -> str:
        normalized = key.strip().lower()
        key_mapping = {
            "arrowleft": "left",
            "arrowright": "right",
            "arrowup": "up",
            "arrowdown": "down",
            "return": "enter",
            "escape": "back",
            "esc": "back",
        }
        return key_mapping.get(normalized, normalized)
