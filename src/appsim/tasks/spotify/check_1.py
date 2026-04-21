# Task 1: 查看当前用户名称
# Check: User profile page is open, username "User" is visible
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("View profile")
        and c.find_text("User")
        and c.find_text("Settings and privacy")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 1)
