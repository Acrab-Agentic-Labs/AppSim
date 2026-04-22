import json
import re
import subprocess
from datetime import date
import os

# 任务24：进入 "机票" 页面，查10月21日从北京飞广州的机票，统计下最便宜的 3 趟航班的平均价格
# 检查条件：智能体计算的平均价格是否与真实的平均价格一致


def check_flight_search_price_avg(result=None, device_id=None,backup_dir=None):
    """
    检验函数：验证智能体答案是否正确

    参数:
        agent_answer: 智能体生成的答案，可以是：
                     - 数字: 625 或 625.0
                     - 字符串: "625" 或 "¥625"
                     - 包含平均价格的字典: {"average_price": 625}

    返回:
        True: 验证成功（允许±1元的误差）
        False: 验证失败
    """
    if result is None:
        return False
    final_message=result.get('final_message')
    if not isinstance(final_message,str):
        return False

    if 'final_message' in result and (
        "625" in result['final_message'] or
        "625.0" in result['final_message'] or
        "￥625" in result['final_message'] or
        "625 元" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == "__main__":

    result=check_flight_search_price_avg()
    print(result)