from ._shared import evaluate_task


def verify_highest_rated_hotel_booking_created(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=2,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_highest_rated_hotel_booking_created())
