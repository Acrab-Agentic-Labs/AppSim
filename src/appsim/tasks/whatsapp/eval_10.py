# Task 10: Check how many statuses the Spotify channel has posted in total and give me an Arabic numeral only.
TASK10_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total number of statuses posted by the Spotify channel.",
    "properties": {
        "status_count": {
            "type": "integer",
            "description": "The total number of statuses posted by the Spotify channel. Must be an Arabic numeral integer.",
        }
    },
    "required": ["status_count"],
    "additionalProperties": False,
}


def validate_task_ten(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("status_count") == 10


if __name__ == "__main__":
    result = validate_task_ten()
    print(result)
