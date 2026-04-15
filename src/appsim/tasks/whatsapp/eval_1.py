# Task 1: Open the first conversation in the chat list, check who sent the latest message, and tell me the name only.
def validate_task_one(result=None, device_id=None, backup_dir=None):
    """Verify task 1: answer "Emily Chen"."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "Emily Chen" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_one()
    print(result)
