# Task 35: 将某条播客快进15s
# Check: Podcast detail page is visible with forward button
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_podcast_fast_forwarded(c: AppChecker):
    passed = (
        c.find_desc("Back")
        and c.find_desc("Forward 15s")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(verify_podcast_fast_forwarded, 35)
