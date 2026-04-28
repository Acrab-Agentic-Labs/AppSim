# Task 18: 查看IRIS OUT的第一句歌词
# Check: Lyrics view is open showing "I close my eyes"
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否在歌词页面
    ui_passed = (
        c.find_desc("Back")
        and c.find_desc("Share")
        and (
            c.find_text_contains("I close my eyes")
            or c.find_text("Lyrics")
        )
    )

    if not ui_passed:
        return result_fail("UI check failed: Lyrics view not visible")

    # 检查 AI 回答是否包含第一句歌词
    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        # 正确答案是 "I close my eyes and see"
        if "i close my eyes and see" in final_msg:
            return result_pass("Check passed: UI correct and answer contains correct first lyric line")
        elif "close" in final_msg and "eyes" in final_msg and "see" in final_msg:
            return result_pass("Check passed: UI correct and answer contains first lyric line")

    return result_fail("Answer check failed: final_message does not contain 'I close my eyes and see'")


if __name__ == "__main__":
    run_check(check, 18)
