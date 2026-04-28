# Task 19: 查看Style的制作人信息，并告诉我作词者是谁
# Check: Credits view is open showing lyricist information
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否在制作信息页面
    ui_passed = (
        c.find_text("Credits")
        and c.find_desc("Back")
        and (
            c.find_text("Performed by")
            or c.find_text("Written by")
            or c.find_text("Produced by")
        )
    )

    if not ui_passed:
        return result_fail("UI check failed: Credits view not visible")

    # 检查 AI 回答是否包含作词者信息
    if result and "final_message" in result:
        final_msg = str(result["final_message"])
        # 正确答案是 "Taylor Swift"
        if "Taylor Swift" in final_msg or "taylor swift" in final_msg.lower():
            return result_pass("Check passed: UI correct and answer contains 'Taylor Swift'")

    return result_fail("Answer check failed: final_message does not contain 'Taylor Swift'")


if __name__ == "__main__":
    run_check(check, 19)
