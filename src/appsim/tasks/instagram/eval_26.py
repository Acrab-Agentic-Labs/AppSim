"""
Check Script #26: 关注首页第三个帖子的作者
Difficulty: 2 (Medium)
Check Method: Read user_state.json to verify the third post's author is followed
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *

# Seed feed order is post_1 anushka, post_2 naina, post_3 yashi; yashi is not followed initially
THIRD_POST_AUTHOR = "user_yashi"


def verify_homepage_third_post_author_followed(adb, ui):
    user = get_user_state(adb)
    if user is None:
        return result_fail("Unable to read user_state.json")

    following = user.get("following", [])
    if THIRD_POST_AUTHOR in following:
        return result_pass(f"{THIRD_POST_AUTHOR} is followed (JSON验证)")
    return result_fail(f"{THIRD_POST_AUTHOR} not in following: {following}")


if __name__ == "__main__":
    run_check(verify_homepage_third_post_author_followed)
