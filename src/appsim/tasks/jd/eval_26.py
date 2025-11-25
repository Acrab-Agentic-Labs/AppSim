def validate_task_twenty_six(result=None, device_id=None, backup_dir=None):
    """验证任务：统计待使用的京东超市的订单总价。"""
    if result and "final_message" in result:
        if "238.6" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_six()
    print(result)
