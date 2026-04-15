from ._shared import evaluate_task


def verify_book_car_pickup_lhr_day_after_tomorrow_noon(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=11,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_book_car_pickup_lhr_day_after_tomorrow_noon())
