"""
Check Script #28: 随机添加一位亲密好友
Difficulty: 2 (Medium)
Check Method: Read user_state.json to verify closeFriends not empty
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        close_friends = user.get("closeFriends", [])
        if close_friends:
            return result_pass(f"Added close friends: {close_friends} (JSON验证)")
        return result_fail("closeFriends is empty, no close friends added")

    # Fallback: UI check
    if ui.has_text("Close friends") and ui.has_text("Remove"):
        return result_pass("Successfully added close friend (Remove button shown)")

    return result_fail("Close friend add action not detected")


if __name__ == "__main__":
    run_check(check)
