def validate_task_twenty_three(result=None, device_id=None, backup_dir=None):
    """验证任务二十三：计算Apple产品京东自营旗舰店评分大于4.7的商品的平均价格，保留一位小数。"""
    # 假设模型会直接在final_message中给出计算结果 "4732.3"
    if result and "final_message" in result:
        if "4732.3" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_three()
    print(result)
