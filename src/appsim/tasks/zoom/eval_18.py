from ._shared import evaluate_task


def verify_nearest_upcoming_meeting_waiting_room_enabled(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=20,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_nearest_upcoming_meeting_waiting_room_enabled())
