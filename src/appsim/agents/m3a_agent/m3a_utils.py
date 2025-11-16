# -*- coding: utf-8 -*-
"""M3A Utility Functions - UI Element Marking and Parsing"""

import re
from typing import Optional, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont


TRIGGER_SAFETY_CLASSIFIER = "Triggered LLM safety classifier."


def validate_ui_element(ui_element, screen_width_height_px: Tuple[int, int]) -> bool:
    """验证 UI 元素是否在屏幕范围内.

    Args:
        ui_element: UI 元素对象
        screen_width_height_px: 屏幕尺寸 (width, height)

    Returns:
        bool: 是否有效
    """
    if not hasattr(ui_element, "bounds"):
        return False

    left, top, right, bottom = ui_element.bounds
    width, height = screen_width_height_px

    # 检查边界是否在屏幕内
    if left < 0 or top < 0 or right > width or bottom > height:
        return False

    # 检查是否有有效尺寸
    if right <= left or bottom <= top:
        return False

    return True


def add_ui_element_mark(
    screenshot: np.ndarray,
    ui_element,
    index: int,
    logical_screen_size: Tuple[int, int],
    physical_frame_boundary: Tuple[int, int, int, int],
    orientation: int,
):
    """在截图上标记 UI 元素（添加边界框和数字索引）.

    Args:
        screenshot: 截图 numpy 数组
        ui_element: UI 元素对象
        index: 元素索引
        logical_screen_size: 逻辑屏幕尺寸
        physical_frame_boundary: 物理帧边界
        orientation: 屏幕方向
    """
    if not validate_ui_element(ui_element, logical_screen_size):
        return

    # 转换为 PIL Image
    if screenshot.dtype != np.uint8:
        screenshot = np.clip(screenshot, 0, 255).astype(np.uint8)

    img = Image.fromarray(screenshot)
    draw = ImageDraw.Draw(img)

    # 获取边界
    left, top, right, bottom = ui_element.bounds

    # 绘制边界框（红色）
    draw.rectangle([left, top, right, bottom], outline="red", width=3)

    # 在左上角绘制索引数字
    try:
        # 尝试使用默认字体
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None

    text = str(index)
    text_bbox = draw.textbbox((0, 0), text, font=font) if font else (0, 0, 20, 20)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 绘制文本背景（白色）
    bg_left = left
    bg_top = top
    bg_right = left + text_width + 4
    bg_bottom = top + text_height + 4
    draw.rectangle([bg_left, bg_top, bg_right, bg_bottom], fill="white", outline="red", width=2)

    # 绘制文本
    draw.text((left + 2, top + 2), text, fill="red", font=font)

    # 转换回 numpy 数组
    screenshot[:] = np.array(img)


def add_screenshot_label(screenshot: np.ndarray, label: str):
    """在截图上添加标签（如 'before' 或 'after'）.

    Args:
        screenshot: 截图 numpy 数组
        label: 标签文本
    """
    if screenshot.dtype != np.uint8:
        screenshot = np.clip(screenshot, 0, 255).astype(np.uint8)

    img = Image.fromarray(screenshot)
    draw = ImageDraw.Draw(img)

    # 获取图片尺寸
    width, height = img.size

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None

    text = label
    text_bbox = draw.textbbox((0, 0), text, font=font) if font else (0, 0, 100, 30)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 在右下角绘制标签
    bg_left = width - text_width - 20
    bg_top = height - text_height - 20
    bg_right = width - 10
    bg_bottom = height - 10

    # 绘制背景
    draw.rectangle([bg_left, bg_top, bg_right, bg_bottom], fill="black", outline="white", width=2)

    # 绘制文本
    draw.text((bg_left + 5, bg_top + 5), text, fill="white", font=font)

    # 转换回 numpy 数组
    screenshot[:] = np.array(img)


def parse_reason_action_output(action_output: str) -> Tuple[Optional[str], Optional[str]]:
    """解析动作输出，提取 reason 和 action.

    Args:
        action_output: LLM 输出的文本

    Returns:
        tuple: (reason, action_json_string)
    """
    reason = None
    action = None

    if not action_output:
        return reason, action

    # 尝试提取 Reason 和 Action
    reason_match = re.search(r"Reason:\s*(.+?)(?:\n|Action:)", action_output, re.DOTALL)
    if reason_match:
        reason = reason_match.group(1).strip()

    # 尝试多种方式提取 JSON action
    # 方式1: Action: {...}
    json_match = re.search(r"Action:\s*(\{.*?\})", action_output, re.DOTALL)
    if json_match:
        action = json_match.group(1).strip()
    else:
        # 方式2: 代码块中的 JSON
        json_block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", action_output, re.DOTALL)
        if json_block_match:
            action = json_block_match.group(1).strip()
        else:
            # 方式3: 直接查找第一个完整的 JSON 对象
            json_obj_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", action_output)
            if json_obj_match:
                action = json_obj_match.group(0).strip()

    # 清理 action 字符串（移除可能的换行和多余空格）
    if action:
        # 尝试解析验证 JSON 格式
        try:
            import json

            # 先尝试直接解析
            json.loads(action)
        except (json.JSONDecodeError, ValueError):
            # 如果失败，尝试清理后再次解析
            # 移除可能的尾随逗号
            action = re.sub(r",\s*}", "}", action)
            action = re.sub(r",\s*]", "]", action)
            # 移除注释（如果存在）
            action = re.sub(r"//.*?$", "", action, flags=re.MULTILINE)
            action = re.sub(r"/\*.*?\*/", "", action, flags=re.DOTALL)
            # 再次尝试解析
            try:
                json.loads(action)
            except (json.JSONDecodeError, ValueError):
                # 如果还是失败，返回 None，让调用者处理
                action = None

    return reason, action
