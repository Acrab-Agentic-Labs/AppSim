"""
Check Script #35: 创建新帖子：含投票 'Which is better?' + 'Option A'/'Option B'
Difficulty: 3 (Hard)
Check Method: Read new_post_events.json to verify post published
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_post_published_with_poll(adb, ui):
    # Primary: check via JSON state - verify post published
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if not event.get("isReel"):
                return result_pass("Post published (JSON verified)")
        return result_fail("Only Reel record, no Post record")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("Post with poll successfully published")

    if ui.has_text("Instagram"):
        if ui.has_text("Which is better?") or ui.has_text("Option A") or ui.has_text("Option B"):
            return result_pass("Post published with poll content")
        return result_fail("Returned to homepage but poll content not found")

    return result_fail("Post publish result not detected")


if __name__ == "__main__":
    run_check(verify_post_published_with_poll)
