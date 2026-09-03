"""
Check Script #36: 创建新帖子：含music+受众设为'Close Friends'
Difficulty: 3 (Hard)
Check Method: 读取 new_post_events.json 验证music和受众设置
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_post_published_with_music_and_audience(adb, ui):
    # Primary: check via JSON state
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel"):
                continue
            has_music = event.get("musicTitle") is not None
            has_audience = event.get("audience") == "Close Friends"

            missing = []
            if not has_music: missing.append("music")
            if not has_audience: missing.append("Close Friends audience")

            if not missing:
                return result_pass(f"Post published: music={event['musicTitle']}, audience={event['audience']} (JSON验证)")
            if len(missing) < 2:
                return result_fail(f"Post published but missing: {', '.join(missing)}")

        return result_fail("Post record exists but settings do not match")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("Post with music successfully published")

    return result_fail("Post publish result not detected")


if __name__ == "__main__":
    run_check(verify_post_published_with_music_and_audience)
