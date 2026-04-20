"""
检测脚本 #10: 滑动查看下一条短视频
难度: 1 (简单)
检测方式: 确认在Reels页面，且当前显示的不是第一个视频
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *

# First reel's author from seed data
FIRST_REEL_AUTHOR = "sangramsinghdeshmukh"


def check(adb, ui):
    # Must be on Reels page (not homepage)
    descs = ui.get_all_descs()
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)

    # Check we're on a Reels full-screen page (not home feed)
    if not ui.has_text("Reels") and found < 3:
        if ui.has_text("Instagram"):
            return result_fail("仍在首页，未进入Reels页面")
        return result_fail("当前不在Reels页面")

    # Verify we're NOT on the first reel (i.e. we swiped)
    # The first reel is by user_sangram (sangramsinghdeshmukh)
    all_texts = ui.get_all_texts()
    if FIRST_REEL_AUTHOR not in " ".join(all_texts):
        return result_pass("已滑动到下一条短视频（不再显示第一个视频的作者）")

    # If first reel author is still visible, check if caption changed
    # Reel 1 caption contains "workout"
    if not any("workout" in t.lower() for t in all_texts):
        return result_pass("已滑动到下一条短视频（内容已变化）")

    return result_fail("仍在第一条短视频，未检测到滑动")


if __name__ == "__main__":
    run_check(check)
