TASK36_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页推荐店铺前20家中起送费低于30元的店铺数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "起送费低于30元的店铺数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def validate_task_thirty_six(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 14
