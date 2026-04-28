# Task 12: 进入随机播放模式
# Check: 通过 JSON 验证随机播放已开启
from .check_common import AppChecker, run_check, result_pass, result_fail


SHUFFLE_VALUES = {"shuffle", "random", "shuffled", "random_play", "shuffle_play", "随机播放", "随机"}


def _is_shuffle_enabled(playback_state):
    if not isinstance(playback_state, dict):
        return False

    for key in ["isShuffle", "shuffle", "shuffleEnabled", "isShuffleEnabled"]:
        if playback_state.get(key) is True:
            return True

    for key in ["playbackMode", "playMode", "mode", "repeatMode"]:
        value = playback_state.get(key)
        if value and str(value).strip().lower() in SHUFFLE_VALUES:
            return True

    return False


def check(c: AppChecker):
    state = c.get_playback_state()
    if _is_shuffle_enabled(state):
        return result_pass("Check passed: shuffle mode is enabled")

    return result_fail(
        "Check failed: shuffle mode is not enabled",
        {"playbackState": state},
    )


if __name__ == "__main__":
    run_check(check, 12)
