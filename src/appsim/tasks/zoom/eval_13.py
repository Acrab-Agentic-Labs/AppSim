from ._shared import evaluate_task


def verify_contact_message_sent_and_recent_chat(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    return evaluate_task(
        task_id=14,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
        **kwargs,
    )


if __name__ == "__main__":
    print(verify_contact_message_sent_and_recent_chat())
