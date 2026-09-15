TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取第一次导航去的地点名称。",
    "properties": {
        "destination_name": {
            "type": "string",
            "description": "第一次导航去的地点完整名称。",
        }
    },
    "required": ["destination_name"],
    "additionalProperties": False,
}


def verify_first_navigation_destination_name(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("destination_name") or "").lower()
    return "lilly cafe" in name
