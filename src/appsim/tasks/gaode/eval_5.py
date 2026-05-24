TASK5_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取收藏夹收藏的地点数量。",
    "properties": {
        "favorite_count": {
            "type": "integer",
            "minimum": 0,
            "description": "收藏夹中收藏的地点数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["favorite_count"],
    "additionalProperties": False,
}


def validate(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("favorite_count") == 3
