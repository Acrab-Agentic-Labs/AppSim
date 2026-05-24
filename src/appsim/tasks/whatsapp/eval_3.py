# Task 3: Check the phone number linked to my account and tell me the answer only.
TASK3_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the phone number linked to the account.",
    "properties": {
        "phone_number": {
            "type": "string",
            "pattern": "^[0-9]{10,15}$",
            "description": "The linked phone number, digits only, without spaces, parentheses, hyphens, or plus signs.",
        }
    },
    "required": ["phone_number"],
    "additionalProperties": False,
}


def validate_task_three(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict):
        phone_number = extracted_answer.get("phone_number")
        if phone_number == "14155550192" or phone_number == "4155550192":
            return True
    return False


if __name__ == "__main__":
    result = validate_task_three()
    print(result)
