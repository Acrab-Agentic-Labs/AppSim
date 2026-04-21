# Task 2: 当前播放歌曲的名称
# Check: Full-screen playing view is open showing song title
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    # Agent should open full-screen playing view to see the song name
    passed = (
        c.find_text("Now Playing")
        and c.find_desc("Album Cover")
    ) or (
        # Or at least mini player is visible with song info
        c.find_desc("Now Playing Cover")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 2)
