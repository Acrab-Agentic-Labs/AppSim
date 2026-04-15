from ._shared import evaluate_task


def verify_book_round_trip_taxi_lhr_hilton_and_return(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=16,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_book_round_trip_taxi_lhr_hilton_and_return())
