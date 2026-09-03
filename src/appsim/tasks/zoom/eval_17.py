from ._shared import evaluate_task

TASK17_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the count of not-started meetings in the next 7 days.",
    "properties": {
        "meeting_count": {
            "type": "integer",
            "minimum": 0,
            "description": "The number of not-started meetings in the next 7 days, as an Arabic numeral integer.",
        }
    },
    "required": ["meeting_count"],
    "additionalProperties": False,
}


def verify_upcoming_meeting_count_and_rename(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=19,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_upcoming_meeting_count_and_rename())
