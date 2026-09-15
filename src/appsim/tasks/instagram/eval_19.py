"""
Check Script #19: 给当前播放的短视频点赞
Difficulty: 2 (Medium)
Check Method: Read reels_state.json to verify reel is liked (not post)
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_current_reel_liked(adb, ui):
    # Primary: check via JSON state — must be a REEL liked, not a post
    reels = get_reels_state(adb)
    if reels:
        for reel in reels:
            if "user_self" in reel.get("likedBy", []):
                return result_pass(f"Reel {reel['reelId']} is liked (JSON verified)")

        # Also verify it wasn't a post that was liked instead
        posts = get_posts_state(adb)
        if posts:
            for post in posts:
                if "user_self" in post.get("likedBy", []):
                    return result_fail(f"Post {post['postId']} 被点赞了，但任务要求给短视频点赞")

        return result_fail("All reels likedBy do not contain user_self")

    # Fallback: UI check — must be on Reels page
    descs = ui.get_all_descs()
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)

    if found < 2:
        if ui.has_text("Instagram"):
            return result_fail("On homepage not Reels page, may have liked a post")
        return result_fail("Not on Reels page")

    if "Unlike" in descs:
        return result_pass("Reel successfully liked (Unlike button found)")

    return result_fail("Reel like success not detected")


if __name__ == "__main__":
    run_check(verify_current_reel_liked)
