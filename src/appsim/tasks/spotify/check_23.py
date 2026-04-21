# Task 23: 打开扫码页面
# Check: Scan Spotify Code page is open
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Scan Spotify Code")
        and c.find_desc("Back")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 23)
