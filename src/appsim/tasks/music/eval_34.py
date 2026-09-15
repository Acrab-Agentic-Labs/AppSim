"""
任务34：告诉我"七里香"的第三条评论是什么
难度：中
类型：信息检索/推理类
"""

import logging
from .verification_functions import read_json_from_device

TASK34_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取歌曲第三条评论的内容。",
    "properties": {
        "comment_content": {
            "type": "string",
            "description": "第三条评论的完整文本内容。",
        }
    },
    "required": ["comment_content"],
    "additionalProperties": False,
}


def verify_third_song_comment_content_reported(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    comment_answer = str(extracted_answer.get("comment_content") or "")
    if not comment_answer:
        return False

    comments_data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments_data:
        return False

    song_comments = None
    all_comments = comments_data.get("allComments", {})
    if isinstance(all_comments, dict):
        if "song_003" in all_comments:
            song_comments = all_comments["song_003"]
        else:
            for song_id, comments in all_comments.items():
                if isinstance(comments, list) and len(comments) > 0:
                    if any("七里香" in str(c) for c in comments):
                        song_comments = comments
                        break

    if not song_comments or len(song_comments) < 3:
        return False

    third_comment = song_comments[2]
    comment_content = third_comment.get("content", "")
    if not comment_content:
        return False

    return comment_content in comment_answer or comment_answer in comment_content
