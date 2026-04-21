"""
Check Script #38: 创建新帖子，hide likes、开启Facebook sharing
Difficulty: 3 (Hard)
Check Method: Read new_post_events.json to verify settings
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Primary: check via JSON state
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel"):
                continue
            hide_likes = event.get("hideLikesAndViews") is True
            fb_share = event.get("shareToFacebook") is True

            missing = []
            if not hide_likes: missing.append("hide likes")
            if not fb_share: missing.append("Facebook sharing")

            if not missing:
                return result_pass("Post published: 点赞数已隐藏+Facebook sharing已开启 (JSON验证)")
            if len(missing) < 2:
                return result_fail(f"Post published but missing: {', '.join(missing)}")

        return result_fail("Post record exists but settings do not match")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("Post successfully published")

    return result_fail("Post publish result not detected")


if __name__ == "__main__":
    run_check(check)
