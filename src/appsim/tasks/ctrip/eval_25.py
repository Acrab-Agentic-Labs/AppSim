import json
import os
import re
import subprocess

# 任务25：进入 "火车票" 页面，查10月22日广州到杭州下午2点到5点的车次，检索这些车次中最高的价格
# 检查条件：智能体返回的价格是否是这些车次中的最高价格

def check_train_search_max_price(result=None, device_id=None):
    """
    检验函数：验证智能体答案是否正确

    参数:
        agent_answer: 智能体生成的答案，可以是：
                     - 数字: 402.5 或 402
                     - 字符串: "402.5" 或 "¥402.5"
                     - 包含价格的字典: {"price": 402.5, "max_price": 402.5}

    返回:
        True: 验证成功（允许±1元的误差）
        False: 验证失败
    """
    if result is None:
        return False
    final_message = result.get('final_message')
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and (
            "402" in result['final_message'] or
            "402.5" in result['final_message'] or
            "￥402" in result['final_message'] or
            "￥402.5" in result['final_message'] or
            "402.5元" in result['final_message'] or
            "402元" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == "__main__":

    result = check_train_search_max_price()
