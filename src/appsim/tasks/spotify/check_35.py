# Task 35: 将某条播客快进15s
# Check: Podcast detail page is visible with forward button
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_desc("Back")
        and c.find_desc("Forward 15s")
    )


if __name__ == "__main__":
    run_check(check, 35)
