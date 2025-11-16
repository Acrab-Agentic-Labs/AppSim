import subprocess
import re


def validate_task_ten(result=None, device_id=None):
    """验证任务十：计算待收货的订单有多少项"""

    # 检查result中的final_message是否包含数字11的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：11个/11项/11份/11件/十一个/十一项/十一份/十一件
        patterns = ["11个", "11项", "11份", "11件", "十一个", "十一项", "十一份", "十一件"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_ten()
    print(result)
