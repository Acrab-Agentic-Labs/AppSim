import json
import subprocess
import os

# 任务22：进入 "酒店" 页面，为我筛选北京评分最高的前 3 家酒店的平均价
# 检查条件：智能体计算的平均价格是否与真实的平均价格一致

TASK22_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取北京评分最高的前3家酒店的平均价格。",
    "properties": {
        "average_price": {
            "type": "integer",
            "description": "平均价格，必须是阿拉伯数字整数，不含货币符号。",
        }
    },
    "required": ["average_price"],
    "additionalProperties": False,
}


def verify_top_rated_hotel_average_price(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    price = extracted_answer.get("average_price")
    return price == 183


if __name__ == "__main__":
    result = verify_top_rated_hotel_average_price()
    print(result)
