TASK19_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the current app version number.",
    "properties": {
        "version": {
            "type": "string",
            "description": "The full app version string, including version prefix and build number.",
        }
    },
    "required": ["version"],
    "additionalProperties": False,
}


def verify_app_version(result=None, **kwargs):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    version = str(extracted_answer.get("version") or "")
    return "v6.311.10000" in version or "6.311.10000" in version
