"""
任务39：收藏歌单"ACG榜"，并播放"夜曲"，收藏歌曲，查看歌词并告诉我第一句歌词是什么，然后查看一下这周的听歌时长
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device

TASK39_ANSWER_SCHEMA = {
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


def verify_playlist_song_actions_lyrics_and_listening_stats(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False

    collected_items = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir)
    if not collected_items:
        return False

    collected_playlists = collected_items.get("collectedPlaylists", []) or collected_items.get("playlists", [])
    acg_collected = any(
        "ACG榜" in p.get("playlistName", "") or "ACG榜" in p.get("name", "") or p.get("playlistId") == "playlist_010"
        for p in collected_playlists
    )
    if not acg_collected:
        return False

    playback_state = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    played_yequ = False
    if playback_state:
        current_song = playback_state.get("currentSong", {})
        if current_song and "夜曲" in current_song.get("songName", ""):
            played_yequ = True
    if not played_yequ and play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
        for record in records:
            if isinstance(record, dict) and ("夜曲" in record.get("songName", "") or "夜曲" in record.get("name", "")):
                played_yequ = True
                break
    if not played_yequ:
        return False

    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("夜曲" in song.get("songName", "") or "夜曲" in song.get("name", "") for song in favorited_songs):
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
    if "我在弹奏萧邦的夜曲" not in first_lyric:
        if "萧邦" not in first_lyric and "夜曲" not in first_lyric:
            return False

    if not app_state.get("listening_stats_viewed", False):
        return False

    return True
