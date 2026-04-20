"""
检测脚本 #19: 给当前播放的短视频点赞
难度: 2 (中等)
检测方式: 读取 reels_state.json 验证 reel 被点赞（不是帖子）
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state — must be a REEL liked, not a post
    reels = get_reels_state(adb)
    if reels:
        for reel in reels:
            if "user_self" in reel.get("likedBy", []):
                return result_pass(f"短视频 {reel['reelId']} 已被点赞 (JSON验证)")

        # Also verify it wasn't a post that was liked instead
        posts = get_posts_state(adb)
        if posts:
            for post in posts:
                if "user_self" in post.get("likedBy", []):
                    return result_fail(f"帖子 {post['postId']} 被点赞了，但任务要求给短视频点赞")

        return result_fail("所有短视频的 likedBy 中都没有 user_self")

    # Fallback: UI check — must be on Reels page
    descs = ui.get_all_descs()
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)

    if found < 2:
        if ui.has_text("Instagram"):
            return result_fail("在首页而非Reels页面，可能给帖子点赞了")
        return result_fail("当前不在Reels页面")

    if "Unlike" in descs:
        return result_pass("短视频已成功点赞（找到Unlike按钮）")

    return result_fail("未检测到短视频点赞成功状态")


if __name__ == "__main__":
    run_check(check)
