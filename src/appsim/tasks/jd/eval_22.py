def validate_task_twenty_two(result=None, device_id=None, backup_dir=None):
    """验证任务：查看评价iPhone15电池续航强的评论有多少。"""

    # 检查result中的final_message是否包含数字1899的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：1899
        patterns = ["1899", "一千八百九十九"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    # This is a placeholder for testing the function directly
    # In actual use, the result dictionary will be passed from the testing framework
    test_result = {"final_message": "评价iPhone15电池续航强的评论有1899条。"}
    result = validate_task_twenty_two(result=test_result)
    print(result)

    test_result_fail = {"final_message": "评价iPhone15电池续航强的评论有1500条。"}
    result = validate_task_twenty_two(result=test_result_fail)
    print(result)
