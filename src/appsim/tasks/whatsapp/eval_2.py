# Task 2: Tell me who the most recent call was with. Just give me the name.
TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the name of the most recent call contact.",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of the person the most recent call was with.",
        }
    },
    "required": ["name"],
    "additionalProperties": False,
}


def validate_task_two(result=None, device_id=None, backup_dir=None):
    """Verify task 2: answer "Sarah Mitchell"."""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    name = str(extracted_answer.get("name") or "")
    return "Sarah Mitchell" in name


if __name__ == "__main__":
    result = validate_task_two()
    print(result)
