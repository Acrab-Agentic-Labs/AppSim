# Task 21: 搜索歌曲shape of you
# Check: Search input contains "shape of you" or search results showing "Shape of You"
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_song_search(c: AppChecker):
    # Check search results page is showing with matching results
    if c.find_text("Search results"):
        passed = c.find_text("Shape of You") or c.find_text_contains("shape of you")
        return result_pass("Check passed") if passed else result_fail("Check failed")

    # Check search input page with relevant text
    if c.find_text("Cancel"):
        text = c.get_edit_text()
        if text and ("shape" in text.lower() or "Shape" in text):
            return result_pass("Search text found")

    # Also accept if search results are showing directly
    passed = c.find_text("Shape of You") or c.find_text_contains("shape of you")
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(verify_song_search, 21)
