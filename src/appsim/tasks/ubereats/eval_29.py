TARGET_VALUE = "14"


def validate_task_twenty_nine(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    normalized_message = final_message.lower()

    if "final_message" in result and (
        "14" in final_message or
        "十四" in final_message or
        "fourteen" in normalized_message
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    print(validate_task_twenty_nine())
