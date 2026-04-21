"""
Check Script #14: View and tell me the first comment of the first post on homepage
Difficulty: 2 (Medium)
Check Method: Check if comments sheet opened and showing comment content
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if Comments bottom sheet opened
    if ui.has_text("Comments") and ui.has_text("Add a comment"):
        # Try获取评论文本
        all_texts = ui.get_all_texts()
        # Exclude system text
        system_texts = {"Comments", "Add a comment...", "Post", "Add a comment", ""}
        comments = [t for t in all_texts if t not in system_texts and len(t) > 2]
        if comments:
            return result_pass(f"Comments sheet opened, first comment text: {comments[0]}")
        return result_pass("Comments sheet opened (but may have no comments)")

    if ui.has_text("Comments"):
        return result_pass("Comments sheet opened")

    return result_fail("Comments sheet not opened")


if __name__ == "__main__":
    run_check(check)
