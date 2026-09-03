"""
任务33：数一下"我喜欢的音乐"里有几首歌曲
难度：中
类型：信息检索类
"""

import logging
from .verification_functions import read_json_from_device

TASK33_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取'我喜欢的音乐'歌单中的歌曲数量。",
    "properties": {
        "song_count": {
            "type": "integer",
            "description": "歌曲数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["song_count"],
    "additionalProperties": False,
}


def verify_favorite_song_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    agent_count = extracted_answer.get("song_count")
    if not isinstance(agent_count, int):
        return False

    favorites_data = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites_data or "favoriteSongs" not in favorites_data or not isinstance(favorites_data.get("favoriteSongs"), list):
        return False

    device_count = len(favorites_data["favoriteSongs"])
    return agent_count == device_count
