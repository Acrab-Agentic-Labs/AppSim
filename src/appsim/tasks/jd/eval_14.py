import re

def validate_task_fourteen(result=None, device_id=None, backup_dir=None):
    """验证任务十四：查看首页华为商品评论数最多的为多少条,给出一个阿拉伯数字即可。"""
    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        numbers = re.findall(r"\d+", message)
        # Check if any of the found numbers is exactly ''
        if '3200' in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
