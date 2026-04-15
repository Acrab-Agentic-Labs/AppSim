# Task 2: Tell me who the most recent call was with. Just give me the name.
def validate_task_two(result=None, device_id=None, backup_dir=None):
    """Verify task 2: answer "Sarah Mitchell"."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "Sarah Mitchell" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_two()
    print(result)
