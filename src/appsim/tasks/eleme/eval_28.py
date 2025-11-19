def validate_task_28(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    # 检测整个 result 中是否包含 "0.75"
    if "final_message" in result and "0.75" in result["final_message"] and "午间" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = validate_task_28()
    print(result)
