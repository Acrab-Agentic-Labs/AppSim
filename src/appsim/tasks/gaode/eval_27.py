def eval_27(result=None, device_id=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "公交586路" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = eval_27()
    print(result)
