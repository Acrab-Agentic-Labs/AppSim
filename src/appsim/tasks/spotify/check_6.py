# Task 6: 告诉我第一条播客的发布时间
# Check: Podcasts page is visible showing the first podcast with date info
# First podcast "How AI is Changing Music" has publish date "Dec 15"
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("How AI is Changing Music")
        and c.find_text_contains("Dec 15")
    )


if __name__ == "__main__":
    run_check(check, 6)
