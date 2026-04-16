# Task 34: 在随机某条播客中发表评论'Great episode!'
# Check: Comment "Great episode!" is visible on the podcast detail page
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return c.find_text("Great episode!")


if __name__ == "__main__":
    run_check(check, 34)
