# Task 11: 播放下一首歌曲
# Check: Full-screen playing view is open (next song was played)
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Now Playing")
        and c.find_desc("Album Cover")
        and c.find_desc("Next")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 11)
