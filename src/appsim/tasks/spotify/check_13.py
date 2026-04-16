# Task 13: 进入单曲循环模式
# Check: Repeat One mode is active in the full-screen playing view
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Now Playing")
        and c.find_desc("Repeat One")
    )


if __name__ == "__main__":
    run_check(check, 13)
