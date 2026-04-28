"""
Check Script #20: 查看个人收藏夹中有几个作品
Difficulty: 2 (Medium)
Check Method: Read JSON files to count saved posts and reels, verify answer
"""
import json
import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def _read_json_from_device(adb, filename):
    """Read JSON file from app's autotest directory"""
    cmd = adb.base_cmd + [
        "exec-out",
        "run-as",
        APP_PACKAGE,
        "cat",
        f"files/autotest/{filename}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0 or not result.stdout.strip():
            return None
        return json.loads(result.stdout)
    except Exception:
        return None


def check(adb, ui, result=None):
    # Read current user ID
    user_state = _read_json_from_device(adb, "user_state.json")
    if not user_state:
        return result_fail("Unable to read user_state.json")

    current_user_id = user_state.get("userId")
    if not current_user_id:
        return result_fail("Unable to get current user ID")

    # Count saved posts
    posts_state = _read_json_from_device(adb, "posts_state.json")
    saved_posts_count = 0
    if posts_state and isinstance(posts_state, list):
        for post in posts_state:
            saved_by = post.get("savedBy", [])
            if current_user_id in saved_by:
                saved_posts_count += 1

    # Count saved reels
    reels_state = _read_json_from_device(adb, "reels_state.json")
    saved_reels_count = 0
    if reels_state and isinstance(reels_state, list):
        for reel in reels_state:
            saved_by = reel.get("savedBy", [])
            if current_user_id in saved_by:
                saved_reels_count += 1

    total_saved = saved_posts_count + saved_reels_count

    # Check if on Saved page (UI validation)
    if not ui.has_text("Saved"):
        return result_fail(
            "Not on Saved page",
            {
                "savedPostsCount": saved_posts_count,
                "savedReelsCount": saved_reels_count,
                "totalSaved": total_saved,
            },
        )

    # Check if AI answer contains the correct count
    if result and "final_message" in result:
        final_msg = str(result["final_message"])
        if str(total_saved) in final_msg:
            return result_pass(
                f"Check passed: UI on Saved page and answer contains correct count ({total_saved})",
                {
                    "savedPostsCount": saved_posts_count,
                    "savedReelsCount": saved_reels_count,
                    "totalSaved": total_saved,
                },
            )

    return result_fail(
        f"Answer check failed: final_message does not contain correct count ({total_saved})",
        {
            "savedPostsCount": saved_posts_count,
            "savedReelsCount": saved_reels_count,
            "totalSaved": total_saved,
        },
    )


if __name__ == "__main__":
    run_check(check)
