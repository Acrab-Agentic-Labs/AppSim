"""
Check Script #12: Search for content related to "happy" on the search page
Difficulty: 2 (Medium)
Check Method: Check if search page displays "happy" search results
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # First confirm if on APP search page (not Chrome or other apps)
    # APP search page should have Search tab and be within Instagram APP
    all_texts = ui.get_all_texts()

    # Check if search results have happy related content
    # Need to exclude cases only in search box, must appear at least 2 places
    happy_count = sum(1 for t in all_texts if "happy" in t.lower())
    if happy_count >= 2:
        return result_pass("Search results contain 'happy' related content")

    # Check if content-desc has happy related content (image descriptions etc)
    descs = ui.get_all_descs()
    happy_desc_count = sum(1 for d in descs if "happy" in d.lower())
    if happy_desc_count > 0 and ui.has_text("happy"):
        return result_pass("Search results contain 'happy' related content (in descs)")

    # Check if on 搜索 page
    if ui.has_text("Search"):
        if ui.has_text("happy"):
            return result_fail("Search box has 'happy' but no results shown")
        return result_fail("On search page but 'happy' search results not found")

    return result_fail("Not on search page")


if __name__ == "__main__":
    run_check(check)
