# Task 13: 进入单曲循环模式
# Check: Repeat One mode is active in the full-screen playing view
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_repeat_one_mode_enabled(c: AppChecker):
    passed = (
        c.find_text("Now Playing")
        and c.find_desc("Repeat One")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(verify_repeat_one_mode_enabled, 13)
