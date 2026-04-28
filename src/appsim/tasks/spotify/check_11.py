# Task 11: 播放下一首歌曲
# Check: 通过 JSON 验证存在下一首行为或当前歌曲已从默认歌曲切换
from .check_common import AppChecker, run_check, result_pass, result_fail


INITIAL_SONG_ID = "song_013"  # IRIS OUT, 默认播放歌曲


def _get_current_song_id(playback_state):
    if not isinstance(playback_state, dict):
        return None

    current_song = playback_state.get("currentSong")
    if isinstance(current_song, dict):
        return current_song.get("id") or current_song.get("songId")

    return playback_state.get("currentSongId") or playback_state.get("songId")


def _is_next_action_value(value):
    if value is None:
        return False
    normalized = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    return normalized in {
        "next",
        "next_song",
        "skip_next",
        "play_next",
        "下一首",
        "切换下一首",
    } or "下一首" in normalized


def _has_next_action(record):
    if not isinstance(record, dict):
        return False

    action_keys = [
        "lastAction",
        "recentAction",
        "lastPlaybackAction",
        "playbackAction",
        "action",
        "type",
        "event",
        "operation",
    ]
    if any(_is_next_action_value(record.get(key)) for key in action_keys):
        return True

    for value in record.values():
        if isinstance(value, dict) and _has_next_action(value):
            return True
        if isinstance(value, list) and any(_has_next_action(item) for item in value[-5:]):
            return True
    return False


def check(c: AppChecker):
    state = c.get_playback_state()
    if not state:
        return result_fail("Check failed: unable to read playback_state.json")

    if _has_next_action(state):
        return result_pass("Check passed: detected next-song action")

    current_song_id = _get_current_song_id(state)
    if current_song_id and current_song_id != INITIAL_SONG_ID:
        return result_pass(f"Check passed: current song changed to {current_song_id}")

    return result_fail(
        "Check failed: no next-song action found and current song did not change from default song",
        {"currentSongId": current_song_id, "playbackState": state},
    )


if __name__ == "__main__":
    run_check(check, 11)
