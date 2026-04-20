"""
Check Script #5: Like the first post on the homepage
Difficulty: 1 (Easy)
Check Method: Read posts_state.json to verify first post has user_self in likedBy
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    posts = get_posts_state(adb)
    if posts:
        original_posts = [p for p in posts if p["postId"].startswith("post_")]
        if original_posts:
            first_post = original_posts[0]
            if "user_self" in first_post.get("likedBy", []):
                return result_pass(f"帖子 {first_post['postId']} 已被点赞 (JSON验证)")
            return result_fail(f"帖子 {first_post['postId']} 的 likedBy 中没有 user_self")

    # Fallback: UI check
    if not ui.has_text("Instagram"):
        return result_fail("Not on homepage")

    descs = ui.get_all_descs()
    if "Unlike" in descs:
        return result_pass("First post liked (Unlike button found)")

    return result_fail("Like success status not detected")


if __name__ == "__main__":
    run_check(check)
