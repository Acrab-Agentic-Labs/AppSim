"""
Check Script #9: 转发第一个帖子
Difficulty: 1 (Easy)
Check Method: Check if repost success prompt appeared (Reposted toast)
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_homepage_first_post_reposted(adb, ui):
    # After repost action should show "Reposted" toast/snackbar
    if ui.has_text("Reposted"):
        return result_pass("Post successfully reposted (Reposted toast appeared)")

    # Check if on首页且转发按钮存在（备选检查）
    if ui.has_text("Instagram"):
        descs = ui.get_all_descs()
        if "Repost" in descs:
            return result_fail("Repost button exists but success not detected")

    return result_fail("Repost success not detected")


if __name__ == "__main__":
    run_check(verify_homepage_first_post_reposted)
