"""
Check Script #20: 查看个人收藏夹中有几个作品
Difficulty: 2 (Medium)
Check Method: Check if on Saved page and can see saved items
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if on Saved page
    if not ui.has_text("Saved"):
        return result_fail("Not on Saved page")

    # Check All Posts collection
    if ui.has_text("All Posts"):
        return result_pass("Opened Saved page with 'All Posts' collection")

    all_texts = ui.get_all_texts()
    # Find收藏数量相关文本
    for text in all_texts:
        if re.match(r'^\d+\s*(items?|posts?|个)', text, re.IGNORECASE):
            return result_pass(f"Saved collection has {text}")

    # On Saved page but saved content not found
    descs = ui.get_all_descs()
    if "Back" in descs:
        return result_pass("Opened Saved page (may be empty)")

    return result_fail("On Saved page but cannot confirm saved content")


if __name__ == "__main__":
    run_check(check)
