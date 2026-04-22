import json
import re
import subprocess
import os

# 任务23：进入 "酒店" 页面，为我检索上海所有酒店中最低的价格
# 检查条件：智能体返回的价格是否是上海所有酒店中的最低价格


def check_hotel_search_shanghai_min_price(result=None, device_id=None,backup_dir=None):
    if result is None:
        return False
    final_message = result.get('final_message')
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and (
            "180" in result['final_message'] or
            "180.0" in result['final_message'] or
            "￥180" in result['final_message'] or
            "180元" in result['final_message']
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result=check_hotel_search_shanghai_min_price()
    print(result)