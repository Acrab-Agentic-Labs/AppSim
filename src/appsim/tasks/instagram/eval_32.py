"""
Check Script #32: 退出当前账号
Difficulty: 3 (Hard)
Check Method: Logout writes no state file, so verify the logged-out screen is shown
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_account_logged_out(adb, ui):
    # Only shown after confirming logout; a failed/empty UI dump must not count as success
    if ui.has_text("You have been logged out"):
        return result_pass("Logged-out screen shown")
    return result_fail("Logged-out screen not detected")


if __name__ == "__main__":
    run_check(verify_account_logged_out)
