def validate_task_seventeen(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    normalized_message = final_message.lower()

    if "final_message" in result and (
        "116.24" in final_message or
        "一百一十六点二四" in final_message or
        "one hundred sixteen point two four" in normalized_message
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    print(validate_task_seventeen())
