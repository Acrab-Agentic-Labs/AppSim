TARGET_VALUE = "18.99"


def validate_task_twenty_seven(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    normalized_message = final_message.lower()

    if "final_message" in result and (
        "18.99" in final_message or
        "十八点九九" in final_message or
        "eighteen point nine nine" in normalized_message
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    print(validate_task_twenty_seven())
