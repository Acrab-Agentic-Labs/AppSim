"""
Check Script #34: 创建新帖子：选第二张图片，caption'Beautiful sunset'，#nature，location'Central Park'
Difficulty: 3 (Hard)
Check Method: Read new_post_events.json to verify post parameters
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_post_published_with_caption_hashtag_location(adb, ui):
    # Primary: check via JSON state
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel"):
                continue
            has_caption = "Beautiful sunset" in (event.get("caption") or "")
            has_hashtag = "nature" in (event.get("hashtags") or [])
            has_location = event.get("location") == "Central Park"

            missing = []
            if not has_caption: missing.append("caption")
            if not has_hashtag: missing.append("#nature hashtag")
            if not has_location: missing.append("location")

            if not missing:
                return result_pass("Post published with all required content (JSON verified)")
            if len(missing) < 3:
                return result_fail(f"Post published but missing: {', '.join(missing)}")

        return result_fail("Post record exists but content does not match")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("Post successfully published (Post shared prompt)")

    if ui.has_text("Instagram"):
        if ui.has_text("Beautiful sunset") or ui.has_text("#nature") or ui.has_text("Central Park"):
            return result_pass("Post published (found post content on homepage)")
        return result_fail("Returned to homepage but post content not found")

    return result_fail("Post publish result not detected")


if __name__ == "__main__":
    run_check(verify_post_published_with_caption_hashtag_location)
