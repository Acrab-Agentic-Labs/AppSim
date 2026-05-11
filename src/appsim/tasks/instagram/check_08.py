"""
Check Script #8: 点赞首页第一条帖子、收藏、评论'Love this!'、转发
Difficulty: 3 (Hard)
Check Method: Read posts_state.json to verify like + save + comment + repost on first post
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    posts = get_posts_state(adb)
    if not posts:
        return result_fail("Unable to read posts_state.json")

    original_posts = [p for p in posts if p["postId"].startswith("post_")]
    if not original_posts:
        return result_fail("No original posts found")

    first_post = original_posts[0]
    checks = {
        "like": "user_self" in first_post.get("likedBy", []),
        "save": "user_self" in first_post.get("savedBy", []),
        "comment": any("Love this!" in c.get("text", "") for c in first_post.get("comments", [])),
        "repost": "user_self" in first_post.get("repostedBy", []),
    }

    missing = [k for k, v in checks.items() if not v]
    if not missing:
        return result_pass("All operations on first post completed (like+save+comment+repost)")
    passed = [k for k, v in checks.items() if v]
    return result_fail(f"Partially completed. Done: {passed}, Missing: {missing}")


if __name__ == "__main__":
    run_check(check)
