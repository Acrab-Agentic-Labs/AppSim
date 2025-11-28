import re


def validate_task_twenty_two(result=None, device_id=None, backup_dir=None):
    """验证任务：查看评价iPhone15电池续航强的评论有多少,给出一个阿拉伯数字即可。"""
    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        # Find all sequences of digits in the message
        numbers = re.findall(r"\d+", message)
        # Check if any of the found numbers is exactly '30'
        if "1899" in numbers:
            return True

    return False


if __name__ == "__main__":
    pass