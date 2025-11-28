import re


def validate_task_twelve(result=None, device_id=None, backup_dir=None):
    """验证任务十二：查看京东秒送的物流消息，确定商品还有多少分钟能送达,给出一个阿拉伯数字即可。"""
    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        # Find all sequences of digits in the message
        numbers = re.findall(r"\d+", message)
        # Check if any of the found numbers is exactly '30'
        if "30" in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
