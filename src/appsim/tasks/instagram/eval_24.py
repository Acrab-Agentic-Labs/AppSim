"""
Check Script #24: 将每日使用时间设置为60min
Difficulty: 2 (Medium)
Check Method: Check if daily time limit on Time Management page is set to 60 minutes
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_daily_usage_limit_set(adb, ui):
    # Check if onTime Management页面
    if not (ui.has_text("Time management") or ui.has_text("daily time limit")):
        return result_fail("Not on Time Management page")

    # Check if shows 60 minutes - need to match "60 min" or "60 minutes"
    all_texts = ui.get_all_texts()
    for text in all_texts:
        if re.search(r'\b60\s*(min|minutes?|分钟)\b', text, re.IGNORECASE):
            return result_pass(f"Daily time limit set to 60 minutes: {text}")

    # Also检查纯 "60" 但要求在 Time limit 上下文中
    if ui.has_text("Set daily time limit") or ui.has_text("Daily time limit"):
        for text in all_texts:
            if text.strip() == "60":
                return result_pass("Daily time limit set to 60 minutes")

    # Check Set daily time limit switch
    if ui.has_text("Set daily time limit"):
        return result_fail("On Time Management page but 60 minutes not detected")

    return result_fail("On Time Management page but 60 minutes setting not found")


if __name__ == "__main__":
    run_check(verify_daily_usage_limit_set)
