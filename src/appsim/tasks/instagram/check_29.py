"""
检测脚本 #29: 移除一位粉丝
难度: 2 (中等)
检测方式: 读取 user_state.json 验证 followers 列表减少
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *

# Initial followers count from seed data
INITIAL_FOLLOWERS_COUNT = 4


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        current_followers = user.get("followers", [])
        current_count = user.get("followersCount", len(current_followers))
        if current_count < INITIAL_FOLLOWERS_COUNT:
            return result_pass(f"粉丝已减少: {INITIAL_FOLLOWERS_COUNT} -> {current_count} (JSON验证)")
        if len(current_followers) < INITIAL_FOLLOWERS_COUNT:
            return result_pass(f"粉丝列表已减少: {INITIAL_FOLLOWERS_COUNT} -> {len(current_followers)} (JSON验证)")
        return result_fail(f"粉丝数未变化，仍为 {current_count}")

    # Fallback: UI check
    if ui.has_text("Removed") or ui.has_text("removed"):
        return result_pass("检测到粉丝已移除的提示")

    return result_fail("未检测到粉丝移除操作结果")


if __name__ == "__main__":
    run_check(check)
