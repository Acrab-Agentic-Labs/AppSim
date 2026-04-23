import json
import re
import subprocess
import os

# 任务22：进入 "酒店" 页面，为我筛选北京评分最高的前 3 家酒店的平均价
# 检查条件：智能体计算的平均价格是否与真实的平均价格一致

def check_hotel_search_beijing_top3_avg_price(result=None,device_id=None, backup_dir=None):

    if result is None:
        return False
    final_message = result.get('final_message')
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and (
            "183" in result['final_message'] or
            "183.0" in result['final_message'] or
            "￥183" in result['final_message'] or
            "183元" in result['final_message']
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    # 计算并打印预期答案
    result=check_hotel_search_beijing_top3_avg_price()
    print(result)
