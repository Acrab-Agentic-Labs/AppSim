import json
import subprocess
import os

# 任务25：进入"火车票"页面，查10月22日广州到杭州下午2点到5点的车次，检索这些车次中最高的价格
# 检查条件：智能体返回的价格是否为 470

TASK25_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取指定车次中最高的价格。",
    "properties": {
        "max_price": {
            "type": "integer",
            "description": "最高价格，必须是阿拉伯数字整数，不含货币符号。",
        }
    },
    "required": ["max_price"],
    "additionalProperties": False,
}


def verify_highest_train_fare(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    price = extracted_answer.get("max_price")
    return price == 470


if __name__ == "__main__":
    print("true" if verify_highest_train_fare() else "false")
