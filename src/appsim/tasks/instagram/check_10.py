"""
Check Script #10: 滑动查看下一条短视频
Difficulty: 1 (Easy)
Check Method: Confirm on Reels page and not showing first video
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *

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
            return result_fail("Still on homepage, not on Reels page")
        return result_fail("Not on Reels page")

    # Verify we're NOT on the first reel (i.e. we swiped)
    # The first reel is by user_sangram (sangramsinghdeshmukh)
    all_texts = ui.get_all_texts()
    if FIRST_REEL_AUTHOR not in " ".join(all_texts):
        return result_pass("Swiped to next reel (first video author no longer shown)")

    # If first reel author is still visible, check if caption changed
    # Reel 1 caption contains "workout"
    if not any("workout" in t.lower() for t in all_texts):
        return result_pass("Swiped to next reel (content changed)")

    return result_fail("Still on first reel, swipe not detected")


if __name__ == "__main__":
    run_check(check)
