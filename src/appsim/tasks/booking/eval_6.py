from ._shared import evaluate_task


def verify_book_again_last_stay_with_no_end_room_note(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=6,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_book_again_last_stay_with_no_end_room_note())
