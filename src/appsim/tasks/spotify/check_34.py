# Task 34: 在随机某条播客中发表评论'Great episode!'
# Check: Comment "Great episode!" is visible on the podcast detail page
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = c.find_text("Great episode!")
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 34)
