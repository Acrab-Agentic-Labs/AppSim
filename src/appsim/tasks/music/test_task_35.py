"""
任务35：搜索'倔强'并播放，收藏该歌曲，查看歌词并告诉我第一句，更改播放器样式，然后创建一个新歌单并添加该歌曲
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device

TASK35_ANSWER_SCHEMA = {
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


def check_composite_juejiang_full(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False

    search_history = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir)
    if not search_history:
        return False

    searched = False
    for search in search_history.get("searches", []):
        if "倔强" in search.get("query", ""):
            searched = True
            break
    if not searched:
        return False

    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("倔强" in song.get("songName", "") or "倔强" in song.get("name", "") for song in favorited_songs):
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
    if "当我和世界不一样" not in first_lyric:
        return False

    player_settings = read_json_from_device("autotest/player_settings.json", device_id, result, backup_dir)
    if not player_settings:
        return False

    if not player_settings.get("style_changed", False):
        return False

    user_playlists = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)
    if not user_playlists:
        return False

    playlists = user_playlists.get("playlists", [])
    if len(playlists) == 0:
        return False

    latest_playlist = playlists[-1]
    song_count = latest_playlist.get("songCount", 0)
    song_ids = latest_playlist.get("songIds", []) or latest_playlist.get("songs", [])
    if song_count == 0 and len(song_ids) == 0:
        return False

    return True
