import json
import subprocess
import os

# 任务23：进入 "酒店" 页面，为我检索上海所有酒店中最低的价格
# 检查条件：智能体返回的价格是否是上海所有酒店中的最低价格

TASK23_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取上海所有酒店中最低的价格。",
    "properties": {
        "min_price": {
            "type": "integer",
            "description": "上海酒店最低价格，必须是阿拉伯数字整数，不含货币符号。",
        }
    },
    "required": ["min_price"],
    "additionalProperties": False,
}


def verify_lowest_hotel_price(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    price = extracted_answer.get("min_price")
    return price == 180


if __name__ == "__main__":
    result = verify_lowest_hotel_price()
    print(result)