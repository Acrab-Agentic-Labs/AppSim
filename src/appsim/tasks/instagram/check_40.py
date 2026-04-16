"""
检测脚本 #40: 发布一条短视频
难度: 3 (困难)
检测方式: 读取 new_post_events.json 验证 isReel=true
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *

INITIAL_REELS_COUNT = 5


def check(adb, ui):
    # Primary: check via new_post_events.json — must be isReel=true
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel") is True:
                return result_pass(f"短视频已发布: {event.get('postId')} (JSON验证)")
        # Events exist but none are reels — published a post instead
        return result_fail("发布了帖子而非短视频 (isReel=false)")

    # Secondary: check reels_state.json for new reels
    reels = get_reels_state(adb)
    if reels and len(reels) > INITIAL_REELS_COUNT:
        return result_pass(f"Reels数量增加到 {len(reels)} (JSON验证)")

    # Fallback: UI check — must see "Reel shared" specifically
    if ui.has_text("Reel shared"):
        return result_pass("短视频已成功发布 (Reel shared)")

    # "Post shared" means a post was published, not a reel
    if ui.has_text("Post shared"):
        return result_fail("发布了帖子而非短视频 (Post shared)")

    if ui.has_text("Instagram"):
        return result_fail("已返回首页，但无法确认短视频是否已发布")

    return result_fail("未检测到短视频发布结果")


if __name__ == "__main__":
    run_check(check)
