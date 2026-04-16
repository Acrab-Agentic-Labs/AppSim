# Task 19: 查看当前歌曲的制作信息
# Check: Credits view is open
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Credits")
        and c.find_desc("Back")
        and (
            c.find_text("Performed by")
            or c.find_text("Written by")
            or c.find_text("Produced by")
        )
    )


if __name__ == "__main__":
    run_check(check, 19)
