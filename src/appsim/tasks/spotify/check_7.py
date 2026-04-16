# Task 7: 告诉我第一本有声书的名字
# Check: Audiobooks page is visible showing "The Art of Reading"
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return c.find_text("The Art of Reading")


if __name__ == "__main__":
    run_check(check, 7)
