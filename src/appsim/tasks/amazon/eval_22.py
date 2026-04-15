def validate_task_twenty_two(result=None, device_id=None, backup_dir=None):
    """Validate task 22: find the three most expensive items in the cart by unit price and calculate their total price."""
    if result and "final_message" in result and result["final_message"] is not None:
        if "3118.98" in result["final_message"]:
            return True
    return False


if __name__ == "__main__":
    result = validate_task_twenty_two()
    print(result)
