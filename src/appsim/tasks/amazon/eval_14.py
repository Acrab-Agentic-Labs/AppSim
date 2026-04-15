def validate_task_fourteen(result=None, device_id=None, backup_dir=None):
    """Validate task 14: view the canceled order and tell me its total amount."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "449.99" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_fourteen()
    print(result)
