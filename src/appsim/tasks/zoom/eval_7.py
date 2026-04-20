from ._shared import evaluate_task


def verify_send_im_lcl_in_new_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=7,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_send_im_lcl_in_new_meeting())
