"""根据 AppSim 的 UI 元素构造 V-Droid 候选动作和文本状态。"""

import json
import re
from html import escape
from typing import Any, Iterable

from ..m3a_agent.u2_env import UIElement

PLACEHOLDER_PATTERN = re.compile(r"^<[^<>]+>$")


def _append_unique(actions: list[str], seen: set[str], action: dict[str, Any]) -> None:
    encoded = json.dumps(action, ensure_ascii=False, separators=(",", ":"))
    if encoded not in seen:
        seen.add(encoded)
        actions.append(encoded)


def build_candidate_actions(
    ui_elements: Iterable[UIElement],
    include_app_switch: bool = True,
) -> list[str]:
    """构造与 V-Droid 官方离散动作空间等价的候选动作。"""

    actions: list[str] = []
    seen: set[str] = set()
    for index, element in enumerate(ui_elements):
        is_checkable = bool(getattr(element, "is_checkable", False))
        if element.is_clickable or is_checkable:
            _append_unique(actions, seen, {"action_type": "click", "index": index})
        if element.is_clickable or element.is_long_clickable:
            _append_unique(actions, seen, {"action_type": "long_press", "index": index})
        if element.is_editable:
            _append_unique(
                actions,
                seen,
                {
                    "action_type": "input_text",
                    "text": "<text_input>",
                    "index": index,
                },
            )
            _append_unique(actions, seen, {"action_type": "clear_text", "index": index})
        if element.is_scrollable:
            for direction in ("up", "down", "left", "right"):
                _append_unique(
                    actions,
                    seen,
                    {
                        "action_type": "scroll",
                        "direction": direction,
                        "index": index,
                    },
                )

    default_actions = [
        {"action_type": "navigate_back"},
        {"action_type": "wait"},
        {"action_type": "status", "goal_status": "complete"},
        {"action_type": "answer", "text": "<answer_text>"},
    ]
    if include_app_switch:
        default_actions[0:0] = [
            {"action_type": "navigate_home"},
            {"action_type": "open_app", "app_name": "<name>"},
        ]

    for action in default_actions:
        _append_unique(actions, seen, action)
    return actions


def _element_label(element: UIElement) -> str:
    for value in (
        element.text,
        element.content_description,
        element.hint_text,
        element.resource_name,
    ):
        if value:
            return str(value).strip()
    return ""


def describe_ui_elements(ui_elements: Iterable[UIElement]) -> str:
    """生成接近 V-Droid 训练输入的扁平 HTML 描述。"""

    lines = ["<div>"]
    for index, element in enumerate(ui_elements):
        label = escape(_element_label(element), quote=True)
        content_description = escape(element.content_description or "", quote=True)
        attributes = [f"id={index}"]
        if content_description:
            attributes.append(f"text='{content_description}'")

        is_checkable = bool(getattr(element, "is_checkable", False))
        if element.is_editable:
            tag = "input"
        elif is_checkable:
            tag = "checkbox"
            attributes.append(f"checked={str(element.is_checked).lower()}")
        elif element.is_clickable or element.is_long_clickable:
            tag = "button"
        elif element.is_scrollable:
            tag = "div"
            attributes.append("scrollable=true")
        else:
            tag = "p"
        lines.append(f"  <{tag} {' '.join(attributes)}>{label}</{tag}>")
    lines.append("</div>")
    return "\n".join(lines)


def parse_action(action: str) -> dict[str, Any]:
    """解析并验证候选动作 JSON。"""

    parsed = json.loads(action)
    if not isinstance(parsed, dict) or not parsed.get("action_type"):
        raise ValueError(f"动作必须是包含 action_type 的 JSON 对象: {action}")
    return parsed


def needs_completion(action: dict[str, Any]) -> bool:
    """判断动作是否仍包含官方占位符。"""

    return any(
        isinstance(value, str) and PLACEHOLDER_PATTERN.fullmatch(value)
        for value in action.values()
    )


def build_rule_summary(action: dict[str, Any], ui_elements: list[UIElement]) -> str:
    """生成不依赖第三方 LLM 的工作记忆。"""

    action_type = action.get("action_type", "unknown")
    index = action.get("index")
    target = ""
    if isinstance(index, int) and 0 <= index < len(ui_elements):
        target = _element_label(ui_elements[index]) or f"index {index}"

    if action_type == "click":
        return f'Clicked "{target}".'
    if action_type == "long_press":
        return f'Long-pressed "{target}".'
    if action_type == "input_text":
        return f'Typed "{action.get("text", "")}" into "{target}".'
    if action_type == "clear_text":
        return f'Cleared text in "{target}".'
    if action_type == "scroll":
        return f'Scrolled {action.get("direction", "")} on "{target or "screen"}".'
    if action_type == "open_app":
        return f'Opened app "{action.get("app_name", "")}".'
    if action_type == "navigate_home":
        return "Navigated to the home screen."
    if action_type == "navigate_back":
        return "Navigated back."
    if action_type == "wait":
        return "Waited for the screen to update."
    if action_type == "answer":
        return f'Answered "{action.get("text", "")}".'
    if action_type == "status":
        return f'Marked task as {action.get("goal_status", "complete")}.'
    return f"Executed {action_type}."
