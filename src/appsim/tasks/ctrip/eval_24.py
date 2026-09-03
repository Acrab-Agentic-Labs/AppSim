import json
import subprocess
import os
from datetime import date

# 任务24：进入 "机票" 页面，查10月21日从北京飞广州的机票，统计下最便宜的 3 趟航班的平均价格
# 检查条件：智能体计算的平均价格是否与真实的平均价格一致

TASK24_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取最便宜的3趟航班的平均价格。",
    "properties": {
        "average_price": {
            "type": "integer",
            "description": "最便宜的3趟航班的平均价格，必须是阿拉伯数字整数，不含货币符号。",
        }
    },
    "required": ["average_price"],
    "additionalProperties": False,
}


def verify_cheapest_flight_average_price(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    price = extracted_answer.get("average_price")
    return price == 625


if __name__ == "__main__":
    result = verify_cheapest_flight_average_price()
    print(result)