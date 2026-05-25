"""
任务37：数一下"热歌榜"里有多少首歌曲
难度：中
类型：信息检索类
"""

import logging
from .verification_functions import read_json_from_device

TASK37_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取'热歌榜'歌单中的歌曲数量。",
    "properties": {
        "song_count": {
            "type": "integer",
            "description": "热歌榜中的歌曲数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["song_count"],
    "additionalProperties": False,
}


def check_hot_rank_song_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    agent_count = extracted_answer.get("song_count")
    if not isinstance(agent_count, int):
        return False

    playlists_data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)
    if not playlists_data or "playlists" not in playlists_data or not isinstance(playlists_data.get("playlists"), list):
        return False

    device_count = 0
    for playlist in playlists_data["playlists"]:
        if playlist.get("playlistName") == "热歌榜":
            device_count = playlist.get("songCount", 0)
            break
    else:
        return False

    return agent_count == device_count
