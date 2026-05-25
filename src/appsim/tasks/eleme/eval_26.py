TASK26_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取9月点外卖次数最多的时间段及其占比。",
    "properties": {
        "ratio": {
            "type": "string",
            "description": "占比数值，用小数表示。仅输出数字。",
        }
    },
    "required": ["ratio"],
    "additionalProperties": False,
}


def validate_task_twenty_six(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    ratio = str(extracted_answer.get("ratio") or "")
    return "0.75" in ratio
