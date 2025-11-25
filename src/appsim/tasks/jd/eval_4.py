def validate_task_four(result=None, device_id=None, backup_dir=None):
    """验证任务四：计算购物车中电子产品的总价"""

    # 检查result中的final_message是否包含相同的数字
    if result and "final_message" in result:
        if "21395" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_four()
    print(result)
