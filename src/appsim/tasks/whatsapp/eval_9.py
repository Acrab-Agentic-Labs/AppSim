# Task 9: Check how many communities I have joined.
TASK9_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of communities the user has joined.",
    "properties": {
        "community_count": {
            "type": "integer",
            "description": "The number of communities joined. Must be an Arabic numeral integer.",
        }
    },
    "required": ["community_count"],
    "additionalProperties": False,
}


def verify_joined_community_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("community_count") == 3


if __name__ == "__main__":
    result = verify_joined_community_count()
    print(result)
