# Task 3: 数一下搜索页面共有多少种分类
# Check: Search page is visible with categories displayed
# Answer: 14 categories (4 in "Start browsing" + 10 in "Browse all")
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Start browsing")
        and c.find_text("Browse all")
    )


if __name__ == "__main__":
    run_check(check, 3)
