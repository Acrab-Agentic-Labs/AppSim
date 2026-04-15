def validate_task_eighteen(result=None, device_id=None, backup_dir=None):
    """Validate task 18: send 'I want to return my order' to customer service, then check and report how many days are mentioned in the reply as the return period."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "30" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_eighteen()
    print(result)
