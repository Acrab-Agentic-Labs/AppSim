from ._shared import evaluate_task


def verify_message_natalie_about_next_monday_leave(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=18,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_message_natalie_about_next_monday_leave())
