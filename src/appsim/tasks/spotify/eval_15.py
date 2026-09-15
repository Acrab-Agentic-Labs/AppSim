# Task 15: 取消当前播放歌曲的收藏
# Check: 通过 JSON 验证存在最近取消收藏行为
from .check_common import AppChecker, run_check, result_pass, result_fail


CURRENT_SONG_ID = "song_013"  # IRIS OUT, 默认播放歌曲


def _is_unlike_action_value(value):
    if value is None:
        return False
    normalized = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    return normalized in {
        "unlike",
        "unliked",
        "remove_like",
        "remove_liked_song",
        "unlike_song",
        "取消收藏",
    } or "取消收藏" in normalized


def _has_unlike_action(record):
    if not isinstance(record, dict):
        return False

    action_keys = ["lastAction", "recentAction", "action", "type", "event", "operation"]
    if any(_is_unlike_action_value(record.get(key)) for key in action_keys):
        return True

    for value in record.values():
        if isinstance(value, dict) and _has_unlike_action(value):
            return True
        if isinstance(value, list) and any(_has_unlike_action(item) for item in value[-5:]):
            return True
    return False


def verify_current_song_unliked(c: AppChecker):
    state = c.get_user_state()
    if not state:
        return result_fail("Check failed: unable to read user_state.json")

    single_value_keys = [
        "recentUnliked",
        "recentUnlikedSong",
        "recentUnlikedSongId",
        "recentUnfavorited",
        "lastUnliked",
        "lastUnlikedSongId",
    ]
    for key in single_value_keys:
        if state.get(key):
            return result_pass(f"Check passed: detected unlike record {key}={state[key]}")

    list_keys = ["unlikedSongs", "unlikeRecords", "unfavoritedSongs"]
    for key in list_keys:
        value = state.get(key)
        if isinstance(value, list) and value:
            return result_pass(f"Check passed: detected unlike record {key}")

    if _has_unlike_action(state):
        return result_pass("Check passed: detected unlike action in user state")

    return result_fail(
        "Check failed: no recent unlike action found in user_state.json",
        {"expectedSongId": CURRENT_SONG_ID, "userState": state},
    )


if __name__ == "__main__":
    run_check(verify_current_song_unliked, 15)
