TASK11_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the current status of restricted mode.",
    "properties": {
        "status": {
            "type": "string",
            "description": "The status of restricted mode, either 'on' or 'off'.",
        }
    },
    "required": ["status"],
    "additionalProperties": False,
}


def verify_restricted_mode_state(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    status = str(extracted_answer.get("status") or "").lower()
    return "off" in status
