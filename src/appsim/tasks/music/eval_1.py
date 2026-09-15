"""
任务1：告诉我用户名是什么
难度：低
类型：信息检索/推理类
"""

import logging
from .verification_functions import read_json_from_device

TASK1_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取当前用户的用户名。",
    "properties": {
        "username": {
            "type": "string",
            "description": "当前用户的用户名，仅输出名称。",
        }
    },
    "required": ["username"],
    "additionalProperties": False,
}


def verify_current_username(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    username_answer = str(extracted_answer.get("username") or "")
    if not username_answer:
        return False

    users_data = read_json_from_device("data/users.json", device_id, result, backup_dir)
    if users_data and isinstance(users_data, list) and len(users_data) > 0:
        username = users_data[0].get("username", "")
    elif users_data and isinstance(users_data, dict):
        username = users_data.get("username", "")
        if not username and "users" in users_data:
            users = users_data["users"]
            if isinstance(users, list) and len(users) > 0:
                username = users[0].get("username", "")
    else:
        username = "音乐爱好者"

    if not username:
        username = "音乐爱好者"

    return username in username_answer or username_answer in username
