TARGET_VALUE = "62.98"


def validate_task_eighteen(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    normalized_message = final_message.lower()

    if "final_message" in result and (
        "62.98" in final_message or
        "六十二点九八" in final_message or
        "sixty-two point nine eight" in normalized_message
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    print(validate_task_eighteen())
