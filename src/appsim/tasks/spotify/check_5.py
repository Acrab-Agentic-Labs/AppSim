# Task 5: 告诉我播客页面第一条播客的标题
# Check: Podcasts page is visible showing first podcast "How AI is Changing Music"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = c.find_text("How AI is Changing Music")
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 5)
