"""
任务38：收藏歌单"国风榜"，并播放"青花瓷"，收藏歌曲，发布评论"真好听"，查看歌曲百科并告诉我曲风是什么
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device

TASK38_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取歌曲的曲风信息。",
    "properties": {
        "genre": {
            "type": "string",
            "description": "歌曲的曲风类型，仅输出曲风名称。",
        }
    },
    "required": ["genre"],
    "additionalProperties": False,
}


def check_composite_guofeng_qinghuaci(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False

    collected_items = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir)
    if not collected_items:
        return False

    collected_playlists = collected_items.get("collectedPlaylists", []) or collected_items.get("playlists", [])
    guofeng_collected = any(
        "国风榜" in p.get("playlistName", "") or "国风榜" in p.get("name", "") or p.get("playlistId") == "playlist_009"
        for p in collected_playlists
    )
    if not guofeng_collected:
        return False

    playback_state = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    played_qinghuaci = False
    if playback_state:
        current_song = playback_state.get("currentSong", {})
        if current_song and "青花瓷" in current_song.get("songName", ""):
            played_qinghuaci = True
    if not played_qinghuaci and play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
        for record in records:
            if isinstance(record, dict) and ("青花瓷" in record.get("songName", "") or "青花瓷" in record.get("name", "")):
                played_qinghuaci = True
                break
    if not played_qinghuaci:
        return False

    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("青花瓷" in song.get("songName", "") or "青花瓷" in song.get("name", "") for song in favorited_songs):
        return False

    comments = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments:
        return False

    user_comments = comments.get("userComments", []) or comments.get("user_comments", [])
    has_comment = any("真好听" in c.get("content", "") for c in user_comments)
    if not has_comment:
        return False

    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state:
        return False

    viewed_song_detail = False
    if app_state.get("currentPage") == "song_detail":
        viewed_song_detail = True
    elif app_state.get("song_detail_viewed", False) or app_state.get("song_encyclopedia_viewed", False):
        viewed_song_detail = True
    else:
        nav_history = app_state.get("navigationHistory", [])
        for record in nav_history:
            page = record.get("page", "") if isinstance(record, dict) else str(record)
            if "song_detail" in page:
                viewed_song_detail = True
                break

    if not viewed_song_detail:
        return False

    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    genre = str(extracted_answer.get("genre") or "")
    if "流行" not in genre and "华语流行" not in genre and "华语" not in genre:
        return False

    return True
