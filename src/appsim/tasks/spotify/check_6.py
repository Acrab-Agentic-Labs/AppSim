# Task 6: 告诉我第一条播客的发布时间
# Check: Podcasts page is visible showing the first podcast with date info
# First podcast "How AI is Changing Music" has publish date "Dec 15"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("How AI is Changing Music")
        and c.find_text_contains("Dec 15")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 6)
