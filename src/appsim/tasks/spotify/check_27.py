# Task 27: 在音乐库中打开Taylor Swift的主页
# Check: Taylor Swift artist page is open
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Taylor Swift")
        and c.find_desc("Back")
        and (
            c.find_text("Popular")
            or c.find_text("Discography")
        )
    )


if __name__ == "__main__":
    run_check(check, 27)
