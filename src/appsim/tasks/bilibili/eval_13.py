TASK13_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取收藏的第一个视频的视频时长。",
    "properties": {
        "duration": {
            "type": "string",
            "description": "视频时长，格式如'03:45'。",
        }
    },
    "required": ["duration"],
    "additionalProperties": False,
}


def validate_task_13(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    duration = str(extracted_answer.get("duration") or "")
    return "03:45" in duration
