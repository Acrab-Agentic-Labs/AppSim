# Task 8: Check how many conversations have unread messages and give me an Arabic numeral only.
TASK8_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of conversations with unread messages.",
    "properties": {
        "unread_count": {
            "type": "integer",
            "description": "The number of conversations with unread messages. Must be an Arabic numeral integer.",
        }
    },
    "required": ["unread_count"],
    "additionalProperties": False,
}


def validate_task_eight(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("unread_count") == 8


if __name__ == "__main__":
    result = validate_task_eight()
    print(result)
