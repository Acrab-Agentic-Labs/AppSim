# Task 26: 播放当前歌曲的下一首, 开启随机播放, 开启单曲循环模式，并收藏歌曲
# Check: 验证 shuffle 和 repeat one 都已启用，likedSongs 增加
from .check_common import AppChecker, run_check, result_pass, result_fail


SHUFFLE_VALUES = {"shuffle", "random", "shuffled", "random_play", "shuffle_play", "随机播放", "随机"}
REPEAT_ONE_VALUES = {"repeat_one", "repeat one", "repeatone", "single", "单曲循环", "单曲"}


def _is_shuffle_enabled(playback_state):
    if not isinstance(playback_state, dict):
        return False

    for key in ["isShuffle", "shuffle", "shuffleEnabled", "isShuffleEnabled"]:
        if playback_state.get(key) is True:
            return True

    for key in ["playbackMode", "playMode", "mode"]:
        value = playback_state.get(key)
        if value and str(value).strip().lower() in SHUFFLE_VALUES:
            return True

    return False


def _is_repeat_one_enabled(playback_state):
    if not isinstance(playback_state, dict):
        return False

    for key in ["isRepeatOne", "repeatOne", "repeatOneEnabled"]:
        if playback_state.get(key) is True:
            return True

    for key in ["repeatMode", "playbackMode", "playMode", "mode"]:
        value = playback_state.get(key)
        if value and str(value).strip().lower() in REPEAT_ONE_VALUES:
            return True

    return False


def verify_playback_controls_and_like(c: AppChecker):
    # 验证 playback_state
    playback_state = c.get_playback_state()
    if not playback_state:
        return result_fail("Check failed: unable to read playback_state.json")

    # 验证 shuffle 已启用
    shuffle_enabled = _is_shuffle_enabled(playback_state)
    if not shuffle_enabled:
        return result_fail(
            "Check failed: shuffle mode is not enabled",
            {"playbackState": playback_state},
        )

    # 验证 repeat one 已启用
    repeat_one_enabled = _is_repeat_one_enabled(playback_state)
    if not repeat_one_enabled:
        return result_fail(
            "Check failed: repeat one mode is not enabled",
            {"playbackState": playback_state},
        )

    # 验证 likedSongs 增加
    user_state = c.get_user_state()
    if not user_state or not isinstance(user_state, dict):
        return result_fail("Check failed: unable to read user_state.json")

    liked_songs = user_state.get("likedSongs", [])
    if len(liked_songs) <= len(c.INITIAL_LIKED_SONGS):
        return result_fail(
            "Check failed: liked songs did not increase",
            {"likedSongs": liked_songs, "initialLikedSongs": c.INITIAL_LIKED_SONGS},
        )

    return result_pass(
        "Check passed: shuffle and repeat one enabled, liked songs increased"
    )


if __name__ == "__main__":
    run_check(verify_playback_controls_and_like, 26)
