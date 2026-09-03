"""
任务18：进入排行榜的新歌榜,告诉我第一首歌名称
难度：中
类型：信息检索类
"""

import logging
from .verification_functions import read_json_from_device

TASK18_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取新歌榜第一首歌的名称。",
    "properties": {
        "song_name": {
            "type": "string",
            "description": "新歌榜第一首歌的完整名称，仅输出歌曲名。",
        }
    },
    "required": ["song_name"],
    "additionalProperties": False,
}


def verify_first_ranked_song_name_reported(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    song_name_answer = str(extracted_answer.get("song_name") or "")
    if not song_name_answer:
        return False

    rankings_data = read_json_from_device("autotest/playlists.json", device_id, result, backup_dir)
    if not rankings_data or "charts" not in rankings_data or not isinstance(rankings_data.get("charts"), list):
        return False

    first_song_name = None
    for chart in rankings_data["charts"]:
        if chart.get("chartName") == "新歌榜":
            if chart.get("songs") and len(chart["songs"]) > 0:
                first_song_name = chart["songs"][0].get("songName")
                break

    if not first_song_name:
        return False

    return first_song_name in song_name_answer or song_name_answer in first_song_name
