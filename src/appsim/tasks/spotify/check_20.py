# Task 20: 查看Style的艺人信息，并告诉我介绍的第一句话是什么
# Check: About the artist view is open showing introduction
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否在艺人信息页面
    ui_passed = (
        c.find_text("About the artist")
        and c.find_desc("Back")
        and (
            c.find_text("Follow")
            or c.find_text_contains("monthly listeners")
        )
    )

    if not ui_passed:
        return result_fail("UI check failed: About the artist view not visible")

    # 检查 AI 回答是否包含介绍的第一句话
    if result and "final_message" in result:
        final_msg = str(result["final_message"])
        # 正确答案是 "Taylor Swift is an American singer-songwriter who has become one of the most influential music artists of the 21st century."
        expected = "Taylor Swift is an American singer-songwriter who has become one of the most influential music artists of the 21st century"
        if expected in final_msg or expected.lower() in final_msg.lower():
            return result_pass("Check passed: UI correct and answer contains correct first sentence")

    return result_fail("Answer check failed: final_message does not contain the correct first sentence about Taylor Swift")


if __name__ == "__main__":
    run_check(check, 20)
