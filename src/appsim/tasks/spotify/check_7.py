# Task 7: 告诉我第一本有声书的名字
# Check: Audiobooks page is visible showing "The Art of Reading"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否显示第一本有声书
    ui_passed = c.find_text("The Art of Reading")

    if not ui_passed:
        return result_fail("UI check failed: First audiobook not visible")

    # 检查 AI 回答是否包含正确的有声书名称
    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        # 正确答案是 "The Art of Reading"
        if "art of reading" in final_msg or ("art" in final_msg and "reading" in final_msg):
            return result_pass("Check passed: UI correct and answer contains audiobook title")

    return result_fail("Answer check failed: final_message does not contain correct audiobook title")


if __name__ == "__main__":
    run_check(check, 7)
