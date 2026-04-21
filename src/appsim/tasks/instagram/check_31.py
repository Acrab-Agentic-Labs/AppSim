"""
Check Script #31: 查看个人主页的第一条视频
Difficulty: 3 (Hard)
Check Method: Check if entered video playback page
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    descs = ui.get_all_descs()

    # Video playback page should have Like/Comment/Share buttons and Back button
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)
    has_back = "Back" in descs

    if found >= 3 and has_back:
        return result_pass("Opened video playback page")

    # Still on profile page (video not clicked)
    if ui.has_text("Edit profile") or ui.has_text("Share profile"):
        if "Reels" in descs or ui.has_text("Reels"):
            return result_fail("On profile Reels tab but specific video not opened")
        return result_fail("On profile but not in video playback")

    # Has Back and some video indicators
    if has_back and found >= 2:
        return result_pass("On video playback/detail page")

    return result_fail("Video playback page not detected")


if __name__ == "__main__":
    run_check(check)
