def validate_task_twenty_one(result=None, device_id=None, backup_dir=None):
    """验证任务：搜索iPhone15并筛选出价格在6000.0至8000.0的手机类别商品有多少个"""

    # 检查result中的final_message是否包含数字3的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：“”
        patterns = ["3个", "3件", "3份", "3项", "三个", "三件", "三份", "三项"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    # This is a placeholder for testing the function directly
    # In actual use, the result dictionary will be passed from the testing framework
    test_result = {"final_message": "筛选后有3个商品"}
    result = validate_task_twenty_one(result=test_result)
    print(result)

    test_result_fail = {"final_message": "筛选后有2个商品"}
    result = validate_task_twenty_one(result=test_result_fail)
    print(result)
