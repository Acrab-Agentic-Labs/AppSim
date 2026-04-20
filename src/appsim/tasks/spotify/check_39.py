# Task 39: 已关注的歌手中，谁的作品数最多
# Check: Agent navigated to library/artist pages to compare works
# Followed artists: Taylor Swift (3 songs), Ed Sheeran (3 songs)
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # Agent should be on an artist page or library page after investigating
    return (
        (c.find_text("Popular") and c.find_desc("Back"))
        or (c.find_text("Discography") and c.find_desc("Back"))
        or c.find_text("Your Library")
    )


if __name__ == "__main__":
    run_check(check, 39)
