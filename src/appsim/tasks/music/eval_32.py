"""
任务32：告诉我"晴天"的第一条评论的发布时间
难度：中
类型：信息检索/推理类
"""

import logging
from datetime import datetime
from .verification_functions import read_json_from_device

TASK32_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取歌曲第一条评论的发布时间。",
    "properties": {
        "comment_time": {
            "type": "string",
            "description": "第一条评论的发布时间，格式如 2024-01-15 或 2024年1月15日。",
        }
    },
    "required": ["comment_time"],
    "additionalProperties": False,
}


def verify_first_song_comment_time_reported(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    comment_time = str(extracted_answer.get("comment_time") or "")
    if not comment_time:
        return False

    comments_data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments_data:
        return False

    song_comments = None
    all_comments = comments_data.get("allComments", {})
    if isinstance(all_comments, dict):
        for song_id, comments in all_comments.items():
            if isinstance(comments, list) and len(comments) > 0:
                if any("晴天" in str(c) for c in comments):
                    song_comments = comments
                    break
        if not song_comments and "song_001" in all_comments:
            song_comments = all_comments["song_001"]
    elif isinstance(all_comments, list):
        song_comments = all_comments

    if not song_comments or len(song_comments) == 0:
        return False

    first_comment = song_comments[0]
    timestamp = first_comment.get("timestamp", 0)
    if not timestamp:
        return False

    try:
        if timestamp > 1e12:
            dt = datetime.fromtimestamp(timestamp / 1000)
        else:
            dt = datetime.fromtimestamp(timestamp)

        possible_formats = [
            dt.strftime("%Y-%m-%d"),
            dt.strftime("%Y年%m月%d日"),
            dt.strftime("%Y/%m/%d"),
            dt.strftime("%m月%d日"),
            dt.strftime("%Y.%m.%d"),
            str(dt.year),
        ]
    except (ValueError, OSError):
        return False

    for fmt in possible_formats:
        if fmt in comment_time:
            return True

    year_str = str(dt.year)
    month_str = str(dt.month)
    day_str = str(dt.day)
    if year_str in comment_time and month_str in comment_time and day_str in comment_time:
        return True

    return False
