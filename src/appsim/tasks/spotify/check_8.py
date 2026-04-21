# Task 8: 告诉我第一本有声书的播放时长
# Check: Audiobook detail view is open showing duration "5h 32min"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("The Art of Reading")
        and c.find_text("5h 32min")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 8)
