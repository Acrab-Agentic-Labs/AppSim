"""
Check Script #2: Tell me how many likes the currently playing short video has
Difficulty: 1 (Easy)
Check Method: Verify if on Reels page, find like count of current reel
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if on Reels page
    descs = ui.get_all_descs()
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)
    if not ui.has_text("Reels") and found < 2:
        return result_fail("Not on Reels page")

    # Find like count: content-desc with "like", e.g. "1.2K likes"
    for desc in descs:
        if re.match(r'^\d+(\.\d+)?[KMkm]?\s*(likes?)', desc.strip(), re.IGNORECASE):
            return result_pass(f"Found like count: {desc}")

    # Find standalone number text (like count usually near Like button)
    all_texts = ui.get_all_texts()
    for text in all_texts:
        if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
            return result_pass(f"Found reel engagement data: {text}")

    return result_fail("Like count not found on reel")


if __name__ == "__main__":
    run_check(check)
