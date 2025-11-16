def eval_34(result=None, device_id=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "11" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = eval_34()
    print(result)
