TASK30_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取前五个订单中由周丹奎配送的订单数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "周丹奎配送的订单数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def validate_task_thirty(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 5
