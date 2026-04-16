"""
检测脚本 #24: 将每日使用时间设置为60min
难度: 2 (中等)
检测方式: 检查Time Management页面的daily time limit是否设为60分钟
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在Time Management页面
    if not (ui.has_text("Time management") or ui.has_text("daily time limit")):
        return result_fail("当前不在时间管理页面")

    # 检查是否显示60分钟 — 需要匹配 "60 min" 或 "60 minutes" 或 "60分钟"
    all_texts = ui.get_all_texts()
    for text in all_texts:
        if re.search(r'\b60\s*(min|minutes?|分钟)\b', text, re.IGNORECASE):
            return result_pass(f"每日使用时间已设置为60分钟: {text}")

    # 也检查纯 "60" 但要求在 Time limit 上下文中
    if ui.has_text("Set daily time limit") or ui.has_text("Daily time limit"):
        for text in all_texts:
            if text.strip() == "60":
                return result_pass("每日使用时间已设置为60分钟")

    # 检查Set daily time limit开关
    if ui.has_text("Set daily time limit"):
        return result_fail("在时间管理页面但未检测到60分钟设置")

    return result_fail("在时间管理页面但未找到60分钟设置")


if __name__ == "__main__":
    run_check(check)
