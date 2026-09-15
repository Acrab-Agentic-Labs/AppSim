"""
任务2：在'我的'页面的所有歌单中哪一个歌单里的歌曲数量最多
难度：中
类型：推理类
"""

import logging
from .verification_functions import read_json_from_device

TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取歌曲数量最多的歌单名称。",
    "properties": {
        "playlist_name": {
            "type": "string",
            "description": "歌曲数量最多的歌单名称，仅输出歌单名。",
        }
    },
    "required": ["playlist_name"],
    "additionalProperties": False,
}


def verify_playlist_with_most_songs(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    playlist_name_answer = str(extracted_answer.get("playlist_name") or "")
    if not playlist_name_answer:
        return False

    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)
    if not data or "playlists" not in data or not data["playlists"]:
        return False

    playlist_with_most_songs = max(data["playlists"], key=lambda p: p.get("songCount", 0))
    most_songs_playlist_name = playlist_with_most_songs.get("playlistName")

    if not most_songs_playlist_name:
        return False

    return most_songs_playlist_name in playlist_name_answer or playlist_name_answer in most_songs_playlist_name
