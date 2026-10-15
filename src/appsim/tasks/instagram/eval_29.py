"""
Check Script #29: 移除粉丝 deepak.patel
Difficulty: 2 (Medium)
Check Method: Read user_state.json to verify user_deepak is no longer a follower
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *

# deepak.patel is one of the three seeded followers
TARGET_FOLLOWER = "user_deepak"


def verify_follower_removed(adb, ui):
    user = get_user_state(adb)
    if user is None:
        return result_fail("Unable to read user_state.json")

    followers = user.get("followers", [])
    if TARGET_FOLLOWER not in followers:
        return result_pass(f"{TARGET_FOLLOWER} removed from followers (JSON验证)")
    return result_fail(f"{TARGET_FOLLOWER} is still a follower: {followers}")


if __name__ == "__main__":
    run_check(verify_follower_removed)
