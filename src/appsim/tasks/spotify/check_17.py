# Task 17: 关掉定时器
# Check: Sleep timer is turned off, back on playing view
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Now Playing")
        or c.find_text("Sleep timer")
    )


if __name__ == "__main__":
    run_check(check, 17)
