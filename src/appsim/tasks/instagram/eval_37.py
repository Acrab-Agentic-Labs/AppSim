"""
Check Script #37: 发布新视频：选择相册第二条视频，标题'cute'，位置Central Park，受众Close Friends
Difficulty: 3 (Hard)
Check Method: Read new_post_events.json to verify video post with correct parameters
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_video_post_published_with_location_and_audience(adb, ui):
    events = get_new_post_events(adb)
    if not events:
        return result_fail("Unable to read new_post_events.json")

    # Find reel/video posts
    reels = [e for e in events if e.get("isReel") is True]
    if not reels:
        return result_fail("No video/reel post found in events")

    latest_reel = reels[-1]
    checks = {
        "caption": "cute" in latest_reel.get("caption", "").lower(),
        "location": "central park" in latest_reel.get("location", "").lower(),
        "audience": latest_reel.get("audience", "").lower() == "close friends",
    }

    missing = [k for k, v in checks.items() if not v]
    if not missing:
        return result_pass("Video posted with correct caption, location, and audience")
    passed = [k for k, v in checks.items() if v]
    return result_fail(f"Partially completed. Done: {passed}, Missing: {missing}", latest_reel)


if __name__ == "__main__":
    run_check(verify_video_post_published_with_location_and_audience)
