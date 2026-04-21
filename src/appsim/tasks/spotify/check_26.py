# Task 26: 打开Liked Songs歌单
# Check: Liked Songs page is open
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Liked Songs")
        and c.find_desc("Back")
        and (
            c.find_desc("Shuffle")
            or c.find_desc("Play")
        )
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 26)
