TASK30_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取搜索原神后第一个视频中点赞最高评论的内容。",
    "properties": {
        "comment_content": {
            "type": "string",
            "description": "点赞最高的评论的完整文字内容。",
        }
    },
    "required": ["comment_content"],
    "additionalProperties": False,
}


def verify_search_first_video_top_comment_content(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    content = str(extracted_answer.get("comment_content") or "")
    return "能不能出一期队伍配置推荐" in content
