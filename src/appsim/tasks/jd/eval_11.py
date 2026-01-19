import re


def validate_task_eleven(result=None, device_id=None, backup_dir=None):
    """验证任务十一：计算我一共收到多少条京东客服的消息，给出一个阿拉伯数字即可。"""

    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        # Find all sequences of digits in the message
        numbers = re.findall(r"\d+", message)
        # Check if any of the found numbers is exactly '2'
        if "2" in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
