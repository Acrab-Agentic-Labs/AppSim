import re


def validate_task_fourteen(result=None, device_id=None, backup_dir=None):
    """验证任务十四：查看首页iPhone15商品共有多少条评论,给出一个阿拉伯数字即可。"""
    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        numbers = re.findall(r"\d+", message)
        # Check if any of the found numbers is exactly ''
        if "3000000" in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
