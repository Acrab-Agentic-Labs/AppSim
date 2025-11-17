def validate_task_twelve(result=None, device_id=None):
    """验证任务十二：查看京东秒送的物流消息，确定商品还有多久能送达"""
    # 检查result中的final_message是否包含时间30的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：30分钟/30min/三十分钟/三十
        patterns = ["30分钟", "30min", "三十分钟", "三十"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_twelve()
    print(result)
