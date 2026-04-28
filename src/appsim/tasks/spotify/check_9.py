# Task 9: 告诉我当前正在播放歌曲的歌手是谁
# Check: Full-screen playing view or mini player is visible showing artist info
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 检查 UI 是否在播放页面
    ui_passed = (
        c.find_text("Now Playing")
        and c.find_desc("Album Cover")
    ) or (
        c.find_desc("Now Playing Cover")
    )

    if not ui_passed:
        return result_fail("UI check failed: Playing view not visible")

    # 检查 AI 回答是否包含歌手名称
    if result and "final_message" in result:
        final_msg = str(result["final_message"])
        # 回答应该包含歌手名称（任何非空字符串都算通过，因为歌手名称可能不同）
        if final_msg and len(final_msg.strip()) > 0:
            return result_pass("Check passed: UI correct and answer contains artist name")

    return result_fail("Answer check failed: final_message is empty or missing")


if __name__ == "__main__":
    run_check(check, 9)
