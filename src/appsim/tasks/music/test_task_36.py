def eval_36(result=None, device_id=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "0" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = eval_36()
    print(result)
