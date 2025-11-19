def validate_task_27(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    # 检测整个 result 中是否包含 "81.5"
    if "final_message" in result and "81.5" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = validate_task_27()
    print(result)
