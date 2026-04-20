"""
检测脚本 #21: 在首页第二个帖子下发布"Nice!"的评论
难度: 2 (中等)
检测方式: 读取 posts_state.json 验证首页第二个帖子的 comments 中包含 "Nice!"
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    posts = get_posts_state(adb)
    if posts:
        # 找首页原始帖子（post_1 ~ post_5），第二个是 post_2
        original_posts = [p for p in posts if p["postId"].startswith("post_")]
        if len(original_posts) >= 2:
            second_post = original_posts[1]
            for comment in second_post.get("comments", []):
                if "Nice!" in comment.get("text", ""):
                    return result_pass(f"评论'Nice!'已在首页第二个帖子 {second_post['postId']} 中发布 (JSON验证)")
            # 也检查其他帖子是否有（可能评论到了错误的帖子）
            for post in original_posts:
                if post["postId"] == second_post["postId"]:
                    continue
                for comment in post.get("comments", []):
                    if "Nice!" in comment.get("text", ""):
                        return result_fail(f"评论'Nice!'发布在了 {post['postId']} 而非第二个帖子 {second_post['postId']}")
            return result_fail("首页帖子的评论中都没有找到'Nice!'")

        # 检查所有帖子
        for post in posts:
            for comment in post.get("comments", []):
                if "Nice!" in comment.get("text", ""):
                    return result_pass(f"评论'Nice!'已在帖子 {post['postId']} 中发布 (JSON验证)")
        return result_fail("所有帖子的评论中都没有找到'Nice!'")

    # Fallback: UI check
    if ui.has_text("Nice!"):
        return result_pass("评论'Nice!'已成功发布")

    return result_fail("未检测到评论'Nice!'")


if __name__ == "__main__":
    run_check(check)
