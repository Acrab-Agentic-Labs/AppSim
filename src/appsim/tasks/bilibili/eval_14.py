TASK14_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取收藏中共收藏了多少个视频。",
    "properties": {
        "video_count": {
            "type": "integer",
            "description": "收藏中的视频总数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["video_count"],
    "additionalProperties": False,
}


def verify_favorite_collection_video_count(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    video_count = extracted_answer.get("video_count")
    return video_count == 10
