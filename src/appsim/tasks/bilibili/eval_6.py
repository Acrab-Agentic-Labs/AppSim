TASK6_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页第一个视频收藏加转发的总数（不算自己的收藏）。",
    "properties": {
        "total": {
            "type": "integer",
            "description": "收藏加转发的总数，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total"],
    "additionalProperties": False,
}


def validate_task_6(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total = extracted_answer.get("total")
    return total == 3999
