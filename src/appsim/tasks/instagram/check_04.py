"""
Check Script #4: Tell me the username of the current user
Difficulty: 1 (Easy)
Check Method: Enter Profile page, extract username information, verify answer
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui, result=None):
    username = None

    # Check if on Profile page
    if ui.has_text("Edit profile") or ui.has_text("Share profile"):
        all_texts = ui.get_all_texts()
        for text in all_texts:
            if text and text not in ["Edit profile", "Share profile", "Posts", "Followers", "Following", "Profile", ""]:
                username = text
                break

    if not username:
        return result_fail("Not on profile page or cannot get username")

    if result and isinstance(result, dict):
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict):
            username_val = str(extracted_answer.get("username") or "")
            if username in username_val:
                return result_pass(f"Current username: {username}, answer correct")

    return result_fail(f"Answer does not contain the username '{username}'")


if __name__ == "__main__":
    run_check(check)
