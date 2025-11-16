def eval_39(result=None, device_id=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "6" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = eval_39()
    print(result)
