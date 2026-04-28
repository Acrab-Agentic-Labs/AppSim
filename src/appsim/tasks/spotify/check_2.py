# Task 2: 当前播放歌曲的名称
# Check: Full-screen playing view is open and answer contains current song title
from .check_common import AppChecker, run_check, result_pass, result_fail


EXPECTED_SONG = "IRIS OUT"


def check(c: AppChecker, result=None):
    # Agent should open full-screen playing view to see the song name
    ui_passed = (
        c.find_text("Now Playing")
        and c.find_desc("Album Cover")
    ) or (
        # Or at least mini player is visible with song info
        c.find_desc("Now Playing Cover")
    )

    if not ui_passed:
        return result_fail("UI check failed: Now Playing view or mini player not visible")

    if result and "final_message" in result:
        final_msg = str(result["final_message"]).lower()
        if EXPECTED_SONG.lower() in final_msg:
            return result_pass("Check passed: UI correct and answer contains current song title")

    return result_fail("Answer check failed: final_message does not contain 'IRIS OUT'")


if __name__ == "__main__":
    run_check(check, 2)
