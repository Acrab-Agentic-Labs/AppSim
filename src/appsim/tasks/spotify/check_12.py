# Task 12: 进入随机播放模式
# Check: Shuffle is enabled in the full-screen playing view
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Now Playing")
        and c.find_desc("Shuffle")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 12)
