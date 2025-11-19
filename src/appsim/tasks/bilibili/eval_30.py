def validate_task_30(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    # 检测 result 中的final_messages中是否包含 "4963"
    if "final_message" in result and "4963" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = validate_task_30()
    print(result)
