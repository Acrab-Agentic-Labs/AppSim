"""
Check Script #40: 发布一条短视频
Difficulty: 3 (Hard)
Check Method: Read new_post_events.json to verify isReel=true
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *

INITIAL_REELS_COUNT = 5


def check(adb, ui):
    # Primary: check via new_post_events.json — must be isReel=true
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel") is True:
                return result_pass(f"Reel published: {event.get('postId')} (JSON验证)")
        # Events exist but none are reels — published a post instead
        return result_fail("发布了帖子而非Reel (isReel=false)")

    # Secondary: check reels_state.json for new reels
    reels = get_reels_state(adb)
    if reels and len(reels) > INITIAL_REELS_COUNT:
        return result_pass(f"Reels count increased to {len(reels)} (JSON验证)")

    # Fallback: UI check — must see "Reel shared" specifically
    if ui.has_text("Reel shared"):
        return result_pass("Reel successfully published (Reel shared)")

    # "Post shared" means a post was published, not a reel
    if ui.has_text("Post shared"):
        return result_fail("发布了帖子而非Reel (Post shared)")

    if ui.has_text("Instagram"):
        return result_fail("Returned to homepage but cannot confirm reel published")

    return result_fail("Reel publish result not detected")


if __name__ == "__main__":
    run_check(check)
