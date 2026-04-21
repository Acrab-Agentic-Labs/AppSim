# Task 3: 数一下搜索页面共有多少种分类
# Check: Search page is visible with categories displayed
# Answer: 14 categories (4 in "Start browsing" + 10 in "Browse all")
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Start browsing")
        and c.find_text("Browse all")
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 3)
