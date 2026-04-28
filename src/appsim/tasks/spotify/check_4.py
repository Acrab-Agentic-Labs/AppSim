# Task 4: 数一下to get you started的第一个推荐歌单有多少首音乐
# Check: Agent opened the first recommended playlist from "To get you started" section
# The first playlist card should be an artist Mix album detail view
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否进入了歌单详情页
    ui_passed = (
        c.find_desc("Back")
        and (
            c.find_text_contains("Mix")
            or c.find_desc("Play")
            or c.find_desc("Shuffle")
        )
    )

    if not ui_passed:
        return result_fail("UI check failed: Playlist detail page not visible")

    # 检查 AI 回答是否包含数字（歌曲数量）
    if result and "final_message" in result:
        final_msg = str(result["final_message"])
        # 提取数字
        import re
        numbers = re.findall(r'\d+', final_msg)
        if numbers:
            return result_pass(f"Check passed: UI correct and answer contains number {numbers[0]}")

    return result_fail("Answer check failed: final_message does not contain song count")


if __name__ == "__main__":
    run_check(check, 4)
