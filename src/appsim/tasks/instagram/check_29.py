"""
Check Script #29: 移除一位粉丝
Difficulty: 2 (Medium)
Check Method: Read user_state.json to verify followers list decreased
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *

# Initial followers count from seed data
INITIAL_FOLLOWERS_COUNT = 4


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        current_followers = user.get("followers", [])
        current_count = user.get("followersCount", len(current_followers))
        if current_count < INITIAL_FOLLOWERS_COUNT:
            return result_pass(f"Followers decreased: {INITIAL_FOLLOWERS_COUNT} -> {current_count} (JSON验证)")
        if len(current_followers) < INITIAL_FOLLOWERS_COUNT:
            return result_pass(f"Followers list decreased: {INITIAL_FOLLOWERS_COUNT} -> {len(current_followers)} (JSON验证)")
        return result_fail(f"Follower count unchanged, still {current_count}")

    # Fallback: UI check
    if ui.has_text("Removed") or ui.has_text("removed"):
        return result_pass("Detected follower removed prompt")

    return result_fail("Follower remove action not detected")


if __name__ == "__main__":
    run_check(check)
