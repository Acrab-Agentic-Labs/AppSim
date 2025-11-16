import json
import subprocess


def validate_task_five(result=None, device_id=None):
    """验证任务五：首页显示的前十个商品中的手机商品的总价是多少？"""
    # 检查result中的final_message是否包含相同的数字
    if result and "final_message" in result:
        if "18985" in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_five()
    print(result)
