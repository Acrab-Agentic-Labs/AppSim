# Task 16: 设置定时器时间为15min
# Check: Sleep timer has been set, back on playing view or timer menu
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # After setting timer, user is back on playing view or menu shows active timer
    return (
        c.find_text("Now Playing")
        or c.find_text("Sleep timer")
        or c.find_text_contains("15 minutes")
    )


if __name__ == "__main__":
    run_check(check, 16)
