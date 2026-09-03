TASK5_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取集合时间和集合地点。",
    "properties": {
        "meeting_time": {
            "type": "string",
            "description": "集合时间，输出格式为 HH:MM（24小时制），例如 09:00。",
        },
        "meeting_location": {
            "type": "string",
            "description": "集合地点名称，仅输出地点，不包含额外描述。",
        },
    },
    "required": ["meeting_time", "meeting_location"],
    "additionalProperties": False,
}


def verify_group_event_details(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    time_val = str(extracted_answer.get("meeting_time") or "").replace("：", ":")
    location_val = str(extracted_answer.get("meeting_location") or "")
    has_time = time_val in ("9:00", "09:00")
    has_location = "香山门口" in location_val
    return has_time and has_location
