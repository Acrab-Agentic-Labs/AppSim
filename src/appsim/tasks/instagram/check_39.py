"""
Check Script #39: 创建新帖子：caption+标签+location+hide likes+turn off comments
Difficulty: 3 (Hard)
Check Method: Read new_post_events.json to verify all settings
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Primary: check via JSON state
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel"):
                continue
            checks = {
                "caption": "Beautiful sunset" in (event.get("caption") or ""),
                "#nature hashtag": "nature" in (event.get("hashtags") or []),
                "location": event.get("location") == "Central Park",
                "hide likes": event.get("hideLikesAndViews") is True,
                "turn off comments": event.get("turnOffComments") is True,
            }
            missing = [k for k, v in checks.items() if not v]

            if not missing:
                return result_pass("Post published with all required settings (JSON verified)")
            if len(missing) < len(checks):
                passed = [k for k, v in checks.items() if v]
                return result_fail(f"Post published, completed: {passed}, missing: {missing}")

        return result_fail("Post record exists but content does not match")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("Post successfully published")

    if ui.has_text("Instagram"):
        if ui.has_text("Beautiful sunset") or ui.has_text("Central Park"):
            return result_pass("Post published, found post content on homepage")
        return result_fail("Returned to homepage but post content not found")

    return result_fail("Post publish result not detected")


if __name__ == "__main__":
    run_check(check)
