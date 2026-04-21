# Task 22: 在搜索页面查看'Music'分类内容
# Check: Music category detail view is open
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_desc("Back")
        and c.find_text("Music")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 22)
