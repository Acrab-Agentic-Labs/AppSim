# Task 7: 告诉我第一本有声书的名字
# Check: Audiobooks page is visible showing "The Art of Reading"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = c.find_text("The Art of Reading")
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 7)
