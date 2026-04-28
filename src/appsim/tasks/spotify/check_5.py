# Task 5: 告诉我播客页面第一条播客的标题
# Check: Podcasts page is visible showing first podcast "How AI is Changing Music"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否显示第一条播客
    ui_passed = c.find_text("How AI is Changing Music")

    if not ui_passed:
        return result_fail("UI check failed: First podcast not visible")

    # 检查 AI 回答是否包含正确的播客标题
    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        # 正确答案是 "How AI is Changing Music"
        if "how ai is changing music" in final_msg or "ai" in final_msg and "music" in final_msg:
            return result_pass("Check passed: UI correct and answer contains podcast title")

    return result_fail("Answer check failed: final_message does not contain correct podcast title")


if __name__ == "__main__":
    run_check(check, 5)
