# Task 8: 告诉我第一本有声书的播放时长
# Check: Audiobook detail view is open showing duration "5h 32min"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否显示有声书详情和时长
    ui_passed = (
        c.find_text("The Art of Reading")
        and c.find_text("5h 32min")
    )

    if not ui_passed:
        return result_fail("UI check failed: Audiobook duration not visible")

    # 检查 AI 回答是否包含正确的时长
    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        # 正确答案是 "5h 32min" 或类似格式
        if ("5" in final_msg and "32" in final_msg) or "5h 32min" in final_msg:
            return result_pass("Check passed: UI correct and answer contains duration")

    return result_fail("Answer check failed: final_message does not contain correct duration")


if __name__ == "__main__":
    run_check(check, 8)
