def eval_38(result=None, device_id=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "13" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = eval_38()
    print(result)
