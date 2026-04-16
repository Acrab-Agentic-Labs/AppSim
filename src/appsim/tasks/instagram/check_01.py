"""
Check Script #1: Tell me how many likes the first post on the homepage has
Difficulty: 1 (Easy)
Check Method: Verify if on homepage, find and extract like count from first post
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Check if on homepage
    if not ui.has_text("Instagram"):
        return result_fail("Not on homepage")

    # Find like count in format: "123 likes" or "1.2K likes"
    all_texts = ui.get_all_texts()
    for text in all_texts:
        if re.match(r'^\d+(\.\d+)?[KMkm]?\s*(likes?|个赞)', text.strip(), re.IGNORECASE):
            return result_pass(f"Found like count: {text}")

    # Check content-desc for like count info
    descs = ui.get_all_descs()
    for desc in descs:
        if re.match(r'^\d+(\.\d+)?[KMkm]?\s*(likes?|个赞)', desc.strip(), re.IGNORECASE):
            return result_pass(f"Found like count in desc: {desc}")

    return result_fail("Like count information not found")


if __name__ == "__main__":
    run_check(check)
