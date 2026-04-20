# Task 22: 在搜索页面查看'Music'分类内容
# Check: Music category detail view is open
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_desc("Back")
        and c.find_text("Music")
    )


if __name__ == "__main__":
    run_check(check, 22)
