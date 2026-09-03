"""
Check Script #26: 关注首页第三个帖子的作者
Difficulty: 2 (Medium)
Check Method: Read user_state.json to verify following list increased
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *

# Initial following list (from users.json seed data)
INITIAL_FOLLOWING = ["user_anushka", "user_naina", "user_deepak", "user_yashi"]


def verify_homepage_third_post_author_followed(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        current_following = user.get("following", [])
        new_follows = [u for u in current_following if u not in INITIAL_FOLLOWING]
        if new_follows:
            return result_pass(f"Newly followed users: {new_follows} (JSON验证)")
        if len(current_following) > len(INITIAL_FOLLOWING):
            return result_pass(f"Following list increased to {len(current_following)} users (JSON verified)")
        return result_fail(f"Following list unchanged, still {len(current_following)} users")

    # Fallback: UI check
    following_nodes = ui.find_by_text("Following")
    if following_nodes:
        return result_pass("Successfully followed user (button shows 'Following')")

    return result_fail("Follow success not detected")


if __name__ == "__main__":
    run_check(verify_homepage_third_post_author_followed)
