# Task 40: 目前音乐库中有多少首喜欢的歌曲
# Check: 通过 JSON 读取实际 likedSongs 数量，并验证答案是否正确
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    state = c.get_user_state()
    if not state:
        return result_fail("Check failed: unable to read user_state.json")

    liked = state.get("likedSongs", [])
    expected_count = len(liked)

    # 检查 UI 是否在 Liked Songs 页面
    ui_passed = (
        c.find_text("Liked Songs")
        and c.find_desc("Back")
        and (
            c.find_text_contains("songs")
            or c.find_desc("Shuffle")
        )
    )

    if not ui_passed:
        return result_fail("UI check failed: Liked Songs page not visible")

    # 检查 AI 回答是否包含正确的数量
    if result and "final_message" in result:
        final_msg = str(result["final_message"])
        # 正确答案应该包含实际数量
        if str(expected_count) in final_msg:
            return result_pass(f"Check passed: UI correct and answer contains {expected_count}")

    return result_fail(
        f"Answer check failed: final_message does not contain correct count ({expected_count})",
        {"likedSongs": liked, "expectedCount": expected_count},
    )


if __name__ == "__main__":
    run_check(check, 40)
