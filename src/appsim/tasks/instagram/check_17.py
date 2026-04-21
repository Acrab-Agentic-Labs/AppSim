"""
Check Script #17: 给首页第一条帖子设置"不感兴趣"
Difficulty: 2 (Medium)
Check Method: Check if menu closed after action (Not interested selected)
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # After action completed, menu should have disappeared
    menu_visible = ui.has_text("Not interested") and ui.has_text("Report")

    if menu_visible:
        # Menu still visible, may not have clicked Not interested
        return result_fail("Menu still visible, 'Not interested' may not be selected")

    # Check snackbar/toast prompt "Not interested" (menu disappeared but feedback remains)
    if ui.has_text("Not interested"):
        return result_pass("Detected Not interested feedback")

    # Menu disappeared and returned to homepage - may be successful or just pressed back
    if ui.has_text("Instagram"):
        # Check if post removed (feed content changed)
        if ui.has_text("Undo"):
            return result_pass("Successfully set 'Not interested' (Undo detected)")
        return result_fail("Returned to homepage but cannot confirm 'Not interested' took effect")

    return result_fail("'Not interested' action not detected")


if __name__ == "__main__":
    run_check(check)
