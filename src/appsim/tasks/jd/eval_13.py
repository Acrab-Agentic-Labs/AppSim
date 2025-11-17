def validate_task_thirteen(result=None, device_id=None):
    """算一下首页前十个商品中，评分大于等于4.7的有几个。"""
    # 检查result中的final_message是否包含数字300的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：'8个','8项','八个', '八项'
        patterns = ["8个", "8项", "八个", "八项"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_thirteen()
    print(result)
