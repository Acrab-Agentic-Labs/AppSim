# Task 12: 进入随机播放模式
# Check: Shuffle is enabled in the full-screen playing view
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Now Playing")
        and c.find_desc("Shuffle")
    )


if __name__ == "__main__":
    run_check(check, 12)
