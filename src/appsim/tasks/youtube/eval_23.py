def validate_task_twenty_three(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    normalized_message = final_message.lower()
    if "final_message" in result and (
        "3.6K" in final_message or
        "3.6k" in final_message or
        "3600" in final_message or
        "three thousand six hundred" in normalized_message
    ):
        return True
    else:
        return False

if __name__ == "__main__":
    print(validate_task_twenty_three())
