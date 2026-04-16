"""
检测脚本 #6: 收藏首页中第一条帖子
难度: 1 (简单)
检测方式: 读取 posts_state.json 验证第一条帖子的 savedBy 包含 user_self
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
            if "user_self" in first_post.get("savedBy", []):
                return result_pass(f"帖子 {first_post['postId']} 已被收藏 (JSON验证)")
            return result_fail(f"帖子 {first_post['postId']} 的 savedBy 中没有 user_self")

    # Fallback: UI check
    if not ui.has_text("Instagram"):
        return result_fail("当前不在首页")

    descs = ui.get_all_descs()
    if "Unsave" in descs:
        return result_pass("帖子已成功收藏（找到Unsave按钮）")

    return result_fail("未检测到收藏成功状态")


if __name__ == "__main__":
    run_check(check)
