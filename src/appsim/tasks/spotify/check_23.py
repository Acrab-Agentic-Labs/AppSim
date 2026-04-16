# Task 23: 打开扫码页面
# Check: Scan Spotify Code page is open
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Scan Spotify Code")
        and c.find_desc("Back")
    )


if __name__ == "__main__":
    run_check(check, 23)
