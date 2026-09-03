from ._shared import evaluate_task

TASK12_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the count of not-started scheduled meetings.",
    "properties": {
        "meeting_count": {
            "type": "integer",
            "minimum": 0,
            "description": "The number of not-started scheduled meetings, as an Arabic numeral integer.",
        }
    },
    "required": ["meeting_count"],
    "additionalProperties": False,
}


def verify_not_started_meeting_count_and_invite_link(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=13,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_not_started_meeting_count_and_invite_link())
