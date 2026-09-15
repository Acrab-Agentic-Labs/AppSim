# Task 1: Open the first conversation in the chat list, check who sent the latest message, and tell me the name only.
TASK1_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the name of the person who sent the latest message.",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of the person who sent the latest message.",
        }
    },
    "required": ["name"],
    "additionalProperties": False,
}


def verify_latest_chat_sender_identified(result=None, device_id=None, backup_dir=None):
    """Verify task 1: answer "Emily Chen"."""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("name") or "")
    return "Emily Chen" in name


if __name__ == "__main__":
    result = verify_latest_chat_sender_identified()
    print(result)
