def eval_29(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "健身私教Lisa" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = eval_29()
    print(result)
