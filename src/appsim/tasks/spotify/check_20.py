# Task 20: 查看当前歌曲的艺人信息
# Check: About the artist view is open
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("About the artist")
        and c.find_desc("Back")
        and (
            c.find_text("Follow")
            or c.find_text_contains("monthly listeners")
        )
    )


if __name__ == "__main__":
    run_check(check, 20)
