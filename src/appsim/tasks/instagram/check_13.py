"""
Check Script #13: 查看消息页面的第一个会话
Difficulty: 2 (Medium)
Check Method: Check if entered chat detail page
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # ChatDetailScreen features: has Back button, Message... input box
    has_back = "Back" in ui.get_all_descs()
    has_message_input = ui.has_text("Message...")

    if has_back and has_message_input:
        return result_pass("Successfully opened first chat conversation")

    # Alternative: 检查Send按钮
    if has_message_input:
        return result_pass("Entered chat detail page")

    # Check if still on messages list
    if ui.has_text("Messages") and not has_message_input:
        return result_fail("Still on messages list, not in conversation detail")

    return result_fail("Chat detail page not detected")


if __name__ == "__main__":
    run_check(check)
