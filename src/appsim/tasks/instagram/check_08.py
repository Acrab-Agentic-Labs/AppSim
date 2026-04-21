"""
Check Script #8: 查看首页中第一个帖子的作者主页
Difficulty: 1 (Easy)
Check Method: Check if entered other user Profile page
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # OtherUserProfileScreen contains Follow/Following button and Message button
    descs = ui.get_all_descs()

    # Check if on 其他用户Profile page
    has_back = "Back" in descs
    has_follow = ui.has_text("Follow") or ui.has_text("Following")
    has_message = ui.has_text("Message")
    has_posts = ui.has_text("Posts")

    if has_back and has_follow and has_message:
        return result_pass("Successfully entered post author profile")

    if has_back and has_posts and (has_follow or ui.has_text("Followers")):
        return result_pass("Entered user profile")

    # Check if has username and post grid
    if has_back and ui.has_text("Followers") and ui.has_text("Following"):
        return result_pass("Entered user profile（含粉丝/关注数据）")

    return result_fail("User profile page not detected")


if __name__ == "__main__":
    run_check(check)
