# Task 3: 数一下搜索页面共有多少种分类
# Check: Search page is visible with categories displayed
# Answer: 14 categories (4 in "Start browsing" + 10 in "Browse all")
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否在搜索页面
    ui_passed = (
        c.find_text("Start browsing")
        and c.find_text("Browse all")
    )

    if not ui_passed:
        return result_fail("UI check failed: Search page not visible")

    # 检查 AI 回答是否包含正确答案
    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        # 正确答案是 14 个分类
        if "14" in final_msg:
            return result_pass("Check passed: UI correct and answer contains 14")

    return result_fail("Answer check failed: final_message does not contain correct answer (14)")


if __name__ == "__main__":
    run_check(check, 3)
