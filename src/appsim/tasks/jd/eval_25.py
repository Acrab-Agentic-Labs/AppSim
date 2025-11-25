def validate_task_twenty_five(result=None, device_id=None, backup_dir=None):
    """验证任务：统计首页前10个商品中不是手机商品的平均评分,保留2位小数。"""
    if result and "final_message" in result:
        # 若在final_message中给出计算结果 "4.78"
        if "4.78" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_five()
    print(result)
