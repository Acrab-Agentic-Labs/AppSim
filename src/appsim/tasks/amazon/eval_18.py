TASK18_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of days mentioned as the return period.",
    "properties": {
        "days": {
            "type": "integer",
            "description": "The number of days for the return period. Must be an Arabic numeral integer.",
        }
    },
    "required": ["days"],
    "additionalProperties": False,
}


def verify_customer_service_return_period(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    days = extracted_answer.get("days")
    if not isinstance(days, int):
        return False
    return days == 30
