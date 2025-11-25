def eval_25(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "11" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = eval_25()
    print(result)
