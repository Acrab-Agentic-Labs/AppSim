# Task 37: 随机收藏一本有声书
# Check: 通过 JSON 验证 savedAudiobooks 数量是否增加（初始为空）
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    state = c.get_user_state()
    if not state:
        return result_fail("Check failed: unable to read user_state.json")

    audiobooks = state.get("savedAudiobooks", [])
    if len(audiobooks) > 0:
        return result_pass("Check passed: a new audiobook was saved")

    return result_fail(
        "Check failed: no saved audiobook found in user_state.json",
        {"savedAudiobooks": audiobooks},
    )


if __name__ == "__main__":
    run_check(check, 37)
