"""
Check Script #6: 收藏首页中第一条帖子
Difficulty: 1 (Easy)
Check Method: Read posts_state.json to verify first post savedBy contains user_self
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_homepage_first_post_saved(adb, ui):
    # Primary: check via JSON state
    posts = get_posts_state(adb)
    if posts:
        original_posts = [p for p in posts if p["postId"].startswith("post_")]
        if original_posts:
            first_post = original_posts[0]
            if "user_self" in first_post.get("savedBy", []):
                return result_pass(f"Post {first_post['postId']} is saved (JSON verified)")
            return result_fail(f"Post {first_post['postId']} savedBy does not contain user_self")

    # Fallback: UI check
    if not ui.has_text("Instagram"):
        return result_fail("Not on homepage")

    descs = ui.get_all_descs()
    if "Unsave" in descs:
        return result_pass("Post successfully saved (Unsave button found)")

    return result_fail("Save success not detected")


if __name__ == "__main__":
    run_check(verify_homepage_first_post_saved)
