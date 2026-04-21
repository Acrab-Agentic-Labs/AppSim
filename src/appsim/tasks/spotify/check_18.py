# Task 18: 查看当前播放歌曲的歌词
# Check: Lyrics view is open
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_desc("Back")
        and c.find_desc("Share")
        and (
            c.find_text_contains("I close my eyes")
            or c.find_text("Lyrics")
        )
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 18)
