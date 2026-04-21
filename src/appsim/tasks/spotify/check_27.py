# Task 27: 在音乐库中打开Taylor Swift的主页
# Check: Taylor Swift artist page is open
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Taylor Swift")
        and c.find_desc("Back")
        and (
            c.find_text("Popular")
            or c.find_text("Discography")
        )
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 27)
