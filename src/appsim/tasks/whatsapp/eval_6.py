# Task 6: Tell me who the most recent video call was with. Just give me the name.
TASK6_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the name of the most recent video call contact.",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of the person the most recent video call was with.",
        }
    },
    "required": ["name"],
    "additionalProperties": False,
}


def verify_latest_video_call_contact_identified(result=None, device_id=None, backup_dir=None):
    """Verify task 6: answer "Marcus Davis"."""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("name") or "")
    return "Marcus Davis" in name


if __name__ == "__main__":
    result = verify_latest_video_call_contact_identified()
    print(result)
