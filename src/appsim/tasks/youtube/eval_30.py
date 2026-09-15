TASK30_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the current app version number.",
    "properties": {
        "version": {
            "type": "string",
            "description": "The app version number string.",
        }
    },
    "required": ["version"],
    "additionalProperties": False,
}


def verify_app_version(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    version = str(extracted_answer.get("version") or "")
    return "21.08.265" in version
