# Task 6: 告诉我第一条播客的发布时间
# Check: Podcasts page is visible showing the first podcast with date info
# First podcast "How AI is Changing Music" has publish date "Dec 15"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否显示播客和日期
    ui_passed = (
        c.find_text("How AI is Changing Music")
        and c.find_text_contains("Dec 15")
    )

    if not ui_passed:
        return result_fail("UI check failed: Podcast date not visible")

    # 检查 AI 回答是否包含正确的日期
    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        # 正确答案是 "Dec 15" 或 "December 15"
        if "dec" in final_msg and "15" in final_msg:
            return result_pass("Check passed: UI correct and answer contains date")

    return result_fail("Answer check failed: final_message does not contain correct date")


if __name__ == "__main__":
    run_check(check, 6)
