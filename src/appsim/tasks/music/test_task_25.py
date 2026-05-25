"""
任务25：搜索'薛之谦'，进入歌手主页，播放"演员"，收藏该歌曲，查看歌词并告诉我第一句歌词，并播放MV
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device

TASK25_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取歌曲的第一句歌词。",
    "properties": {
        "first_lyric": {
            "type": "string",
            "description": "歌曲的第一句歌词内容，仅输出歌词文本。",
        }
    },
    "required": ["first_lyric"],
    "additionalProperties": False,
}


def check_composite_xuezhiqian_play_favorite_lyrics_mv(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False

    search_history = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir)
    if not search_history:
        return False

    searched = False
    for search in search_history.get("searches", []):
        if "薛之谦" in search.get("query", ""):
            searched = True
            break
    if not searched:
        return False

    playback_state = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    if not playback_state:
        return False

    current_song = playback_state.get("currentSong", {})
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    played_yangyuan = False
    if current_song and "演员" in current_song.get("songName", ""):
        played_yangyuan = True
    elif play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
        for record in records:
            if isinstance(record, dict) and ("演员" in record.get("songName", "") or "演员" in record.get("name", "")):
                played_yangyuan = True
                break
    if not played_yangyuan:
        return False

    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("演员" in song.get("songName", "") or "演员" in song.get("name", "") for song in favorited_songs):
        return False

    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state:
        return False

    if not app_state.get("lyrics_shown", False) and not app_state.get("showLyrics", False):
        return False

    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    first_lyric = str(extracted_answer.get("first_lyric") or "")
    if "简单点说话的方式简单点" not in first_lyric:
        return False

    mv_state = read_json_from_device("autotest/mv_playback.json", device_id, result, backup_dir)
    if not mv_state:
        return False

    if not mv_state.get("is_playing", False) and not mv_state.get("isPlaying", False):
        return False

    return True
