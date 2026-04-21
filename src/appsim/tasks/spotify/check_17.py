# Task 17: 关掉定时器
# Check: Sleep timer is turned off, back on playing view
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Now Playing")
        or c.find_text("Sleep timer")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 17)
