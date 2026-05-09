# -*- coding: utf-8 -*-
"""AgentCPM-GUI 动作解析和校验工具。"""

import json
import re
from typing import Any, Dict, List, Tuple

DEFAULT_DURATION_MS = 200
LONG_PRESS_THRESHOLD_MS = 200
SUCCESS_STATUSES = {"finish", "satisfied"}
FAILURE_STATUSES = {"impossible", "interrupt", "need_feedback"}
CONTINUE_STATUSES = {"continue", "start"}
VALID_STATUSES = SUCCESS_STATUSES | FAILURE_STATUSES | CONTINUE_STATUSES
VALID_PRESS_KEYS = {"HOME", "BACK", "ENTER"}
VALID_DIRECTIONS = {"up", "down", "left", "right"}


def clamp(value: int, lower: int, upper: int) -> int:
    """将数值限制在闭区间内。"""
    return max(lower, min(value, upper))


def rescale_point(point: List[int], width: int, height: int) -> Tuple[int, int]:
    """将 AgentCPM-GUI 的 0-1000 坐标缩放到真实屏幕像素坐标。"""
    x = int(point[0] / 1000 * width)
    y = int(point[1] / 1000 * height)
    return clamp(x, 0, width - 1), clamp(y, 0, height - 1)


def extract_json_object(response_text: str) -> Dict[str, Any]:
    """从模型输出中提取紧凑 JSON 对象。"""
    if not response_text:
        raise ValueError("模型输出为空")

    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise
        parsed = json.loads(match.group(0))

    if not isinstance(parsed, dict):
        raise ValueError(f"模型输出不是 JSON 对象: {type(parsed)}")
    return parsed


def validate_agentcpm_action(action: Dict[str, Any]) -> None:
    """轻量校验 AgentCPM-GUI 输出，避免执行明显非法的动作。"""
    allowed_keys = {"thought", "POINT", "to", "duration", "PRESS", "TYPE", "STATUS"}
    unknown_keys = set(action) - allowed_keys
    if unknown_keys:
        raise ValueError(f"动作包含未知字段: {sorted(unknown_keys)}")

    primitives = [key for key in ("POINT", "PRESS", "TYPE") if key in action]
    status = action.get("STATUS", "continue")

    if status not in VALID_STATUSES:
        raise ValueError(f"未知 STATUS: {status}")
    if len(primitives) > 1:
        raise ValueError(f"动作包含多个原子操作: {primitives}")
    if status in CONTINUE_STATUSES and not primitives and "duration" not in action:
        raise ValueError("continue/start 状态必须携带原子操作或等待 duration")

    if "POINT" in action and not _is_valid_point(action["POINT"]):
        raise ValueError(f"非法 POINT: {action['POINT']}")
    if "to" in action:
        if "POINT" not in action:
            raise ValueError("to 字段必须与 POINT 一起出现")
        to = action["to"]
        if not ((isinstance(to, str) and to in VALID_DIRECTIONS) or _is_valid_point(to)):
            raise ValueError(f"非法 to 字段: {to}")
    if "duration" in action:
        duration = action["duration"]
        if not isinstance(duration, int) or duration < 0:
            raise ValueError(f"非法 duration: {duration}")
    if "PRESS" in action and action["PRESS"] not in VALID_PRESS_KEYS:
        raise ValueError(f"非法 PRESS: {action['PRESS']}")
    if "TYPE" in action and not isinstance(action["TYPE"], str):
        raise ValueError("TYPE 必须是字符串")


def _is_valid_point(point: Any) -> bool:
    if not isinstance(point, list) or len(point) != 2:
        return False
    return all(isinstance(value, int) and 0 <= value <= 1000 for value in point)
