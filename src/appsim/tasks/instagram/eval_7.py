"""
Check Script #7: 打开通知页面
Difficulty: 1 (Easy)
Check Method: Check if currently on Notifications page
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_notifications_page_opened(adb, ui):
    # Check if on 通知 page
    if ui.has_text("Notifications"):
        # Further确认页面特征
        if ui.has_text("Follow requests") or ui.has_text("This month") or ui.has_text("Earlier"):
            return result_pass("Successfully opened notifications page (with full content)")
        return result_pass("Successfully opened notifications page")

    return result_fail("Not on notifications page")


if __name__ == "__main__":
    run_check(verify_notifications_page_opened)
