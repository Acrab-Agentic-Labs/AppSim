# Task 2: 当前播放歌曲的名称
# Check: Full-screen playing view is open showing song title
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # Agent should open full-screen playing view to see the song name
    return (
        c.find_text("Now Playing")
        and c.find_desc("Album Cover")
    ) or (
        # Or at least mini player is visible with song info
        c.find_desc("Now Playing Cover")
    )


if __name__ == "__main__":
    run_check(check, 2)
