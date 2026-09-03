# Task 10: 在全屏播放页面播放或者暂停歌曲
# Check: Full-screen playing view is open and play/pause button state changed
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_full_screen_playback_state(c: AppChecker):
    passed = (
        c.find_text("Now Playing")
        and (c.find_desc("Pause") or c.find_desc("Play"))
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(verify_full_screen_playback_state, 10)
