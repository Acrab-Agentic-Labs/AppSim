"""
Check Script #27: 随机选择一位用户并拉黑
Difficulty: 2 (Medium)
Check Method: Read user_state.json to verify blockedUsers not empty
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_user_blocked(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        blocked = user.get("blockedUsers", [])
        if blocked:
            return result_pass(f"Blocked users: {blocked} (JSON验证)")
        return result_fail("blockedUsers is empty, no users blocked")

    # Fallback: UI check
    if ui.has_text("Blocked") and ui.has_text("Unblock"):
        return result_pass("Successfully blocked user (users in Blocked list)")

    return result_fail("Block action not detected")


if __name__ == "__main__":
    run_check(verify_user_blocked)
