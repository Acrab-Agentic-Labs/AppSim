# Task 6: Tell me who the most recent video call was with. Just give me the name.
def validate_task_six(result=None, device_id=None, backup_dir=None):
    """Verify task 6: answer "Marcus Davis"."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "Marcus Davis" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_six()
    print(result)
