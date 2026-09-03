"""
Check Script #25: 修改username为"zhou"
Difficulty: 2 (Medium)
Check Method: Check if username in user_state.json or UI is "zhou"
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_username_changed(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        username = user.get("username", "")
        if username.lower() == "zhou":
            return result_pass(f"username changed to '{username}' (JSON verified)")
        return result_fail(f"username still '{username}', not changed to 'zhou'")

    # Fallback: UI check
    if ui.has_text("zhou"):
        if ui.has_text("Edit profile") or ui.has_text("Share profile"):
            return result_pass("Page shows username 'zhou'")
        return result_pass("Detected 'zhou' text")

    if ui.has_text("Edit profile"):
        return result_fail("On Edit Profile page but username is not 'zhou'")

    return result_fail("username 'zhou' not detected")


if __name__ == "__main__":
    run_check(verify_username_changed)
