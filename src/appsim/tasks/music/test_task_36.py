"""
任务36：数一下我的粉丝数目
难度：中
类型：信息检索类
"""

import logging
from .verification_functions import read_json_from_device

TASK36_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取用户的粉丝数目。",
    "properties": {
        "fan_count": {
            "type": "integer",
            "description": "粉丝数目，必须是阿拉伯数字整数。",
        }
    },
    "required": ["fan_count"],
    "additionalProperties": False,
}


def check_fan_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    agent_count = extracted_answer.get("fan_count")
    if not isinstance(agent_count, int):
        return False

    fan_items_data = read_json_from_device("autotest/fan_items.json", device_id, result, backup_dir)
    if not isinstance(fan_items_data, list):
        return False

    device_count = len(fan_items_data)
    return agent_count == device_count
