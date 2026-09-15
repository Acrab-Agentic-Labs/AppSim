TASK27_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the selected option for Video quality on mobile networks.",
    "properties": {
        "quality_option": {
            "type": "string",
            "description": "The selected video quality option text.",
        }
    },
    "required": ["quality_option"],
    "additionalProperties": False,
}


def verify_mobile_network_video_quality(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    option = str(extracted_answer.get("quality_option") or "")
    return "Auto" in option
