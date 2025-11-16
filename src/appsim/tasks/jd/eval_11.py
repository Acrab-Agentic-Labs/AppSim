import subprocess
import re


def validate_task_eleven(result=None, device_id=None):
    """验证任务十一：计算我一共收到多少条京东客服的消息"""

    # 检查result中的final_message是否包含数字2的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：2条/2份/2个/两条/两份/两个
        patterns = ["2条", "2份", "2个", "两条", "两份", "两个"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_eleven()
    print(result)
