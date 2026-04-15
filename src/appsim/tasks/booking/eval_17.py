from ._shared import evaluate_task


def verify_book_most_comfortable_taxi_hkg_to_regal(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=17,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )


if __name__ == "__main__":
    print(verify_book_most_comfortable_taxi_hkg_to_regal())
