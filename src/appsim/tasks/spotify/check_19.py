# Task 19: 查看当前歌曲的制作信息
# Check: Credits view is open
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Credits")
        and c.find_desc("Back")
        and (
            c.find_text("Performed by")
            or c.find_text("Written by")
            or c.find_text("Produced by")
        )
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 19)
