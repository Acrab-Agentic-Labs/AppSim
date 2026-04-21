# Task 20: 查看当前歌曲的艺人信息
# Check: About the artist view is open
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("About the artist")
        and c.find_desc("Back")
        and (
            c.find_text("Follow")
            or c.find_text_contains("monthly listeners")
        )
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 20)
