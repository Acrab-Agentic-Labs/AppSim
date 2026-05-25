from ._shared import evaluate_task

TASK21_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract information about the nearest upcoming trip.",
    "properties": {
        "trip_name": {
            "type": "string",
            "description": "The name or title of the nearest upcoming trip.",
        },
        "trip_date": {
            "type": "string",
            "description": "The date of the trip.",
        },
        "trip_amount": {
            "type": "string",
            "description": "The cost/amount of the trip.",
        },
    },
    "required": ["trip_name"],
    "additionalProperties": False,
}


def verify_answer_nearest_upcoming_trip(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=21,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_answer_nearest_upcoming_trip())
