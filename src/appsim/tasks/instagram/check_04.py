"""
Check Script #4: Tell me the username of the current user
Difficulty: 1 (Easy)
Check Method: Enter Profile page, extract username information
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if on Profile page
    if ui.has_text("Edit profile") or ui.has_text("Share profile"):
        # On Profile page, username usually shown at top
        all_texts = ui.get_all_texts()
        # Username usually first non-empty text or text with @ prefix
        for text in all_texts:
            if text and text not in ["Edit profile", "Share profile", "Posts", "Followers", "Following", "Profile", ""]:
                return result_pass(f"Current username: {text}")

    # Also可能在其他页面，检查顶部caption栏
    descs = ui.get_all_descs()
    for desc in descs:
        if desc == "Profile":
            return result_fail("On Profile tab but unable to extract username")

    return result_fail("Not on profile page，Cannot get username")


if __name__ == "__main__":
    run_check(check)
