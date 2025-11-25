def browsing_history_check(result=None, device_id=None,backup_dir=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "收藏" and "秋冬" and "穿搭" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = browsing_history_check()
    print(result)
