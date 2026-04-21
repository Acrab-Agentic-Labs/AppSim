"""
Check Script #21: 在首页第二个帖子下发布"Nice!"的评论
Difficulty: 2 (Medium)
Check Method: Read posts_state.json to verify second homepage post comments contain "Nice!"
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Primary: check via JSON state
    posts = get_posts_state(adb)
    if posts:
        # Find original homepage posts (post_1 ~ post_5), second is post_2
        original_posts = [p for p in posts if p["postId"].startswith("post_")]
        if len(original_posts) >= 2:
            second_post = original_posts[1]
            for comment in second_post.get("comments", []):
                if "Nice!" in comment.get("text", ""):
                    return result_pass(f"评论'Nice!'已在首页第二个Post {second_post['postId']} (JSON verified)")
            # Also检查其他帖子是否有（可能评论到了错误的帖子）
            for post in original_posts:
                if post["postId"] == second_post["postId"]:
                    continue
                for comment in post.get("comments", []):
                    if "Nice!" in comment.get("text", ""):
                        return result_fail(f"Comment 'Nice!' posted on {post['postId']} 而非第二个Post {second_post['postId']}")
            return result_fail("'Nice!' not found in any homepage post comments")

        # Check all posts
        for post in posts:
            for comment in post.get("comments", []):
                if "Nice!" in comment.get("text", ""):
                    return result_pass(f"评论'Nice!'已在Post {post['postId']} (JSON verified)")
        return result_fail("'Nice!' not found in any post comments")

    # Fallback: UI check
    if ui.has_text("Nice!"):
        return result_pass("Comment 'Nice!' successfully posted")

    return result_fail("Comment 'Nice!' not detected")


if __name__ == "__main__":
    run_check(check)
