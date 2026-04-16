# Task 21: 搜索歌曲shape of you
# Check: Search input contains "shape of you" or search results showing "Shape of You"
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # Check search results page is showing with matching results
    if c.find_text("Search results"):
        return c.find_text("Shape of You") or c.find_text_contains("shape of you")
    # Check search input page with relevant text
    if c.find_text("Cancel"):
        text = c.get_edit_text()
        if text and ("shape" in text.lower() or "Shape" in text):
            return True
    # Also accept if search results are showing directly
    return c.find_text("Shape of You") or c.find_text_contains("shape of you")


if __name__ == "__main__":
    run_check(check, 21)
