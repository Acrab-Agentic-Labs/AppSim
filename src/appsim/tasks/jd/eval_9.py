def validate_task_nine(result=None, device_id=None):
    """验证任务九：计算购物车中所有商品的总价"""

    # 检查result中的final_message是否包含相同的数字
    if result and "final_message" in result:
        if "23338" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_nine()
    print(result)
