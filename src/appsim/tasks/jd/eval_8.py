def validate_task_eight(result=None, device_id=None):
    """验证任务八：计算首页展示的商品中前十个有多少个是手机。"""

    # 检查result中的final_message是否包含数字4的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：4个/4件/4份/4项/四个/四件/四份/四项
        patterns = ["4个", "4件", "4份", "4项", "四个", "四件", "四份", "四项"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_eight()
    print(result)
