"""
任务1：告诉我用户名是什么
难度：低
类型：信息检索/推理类
"""

import logging
import re
from .verification_functions import read_json_from_device


def check_username_is_reported(result=None, device_id=None, backup_dir=None):
    """
    任务1: 验证AI是否返回了正确的用户名
    - 从AI的 final_message 中检查是否包含正确的用户名
    - 从设备读取用户数据获取真实用户名
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务1未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务1未完成：final_message格式错误: {final_msg}")
        return False

    # 从设备读取用户数据
    users_data = read_json_from_device("data/users.json", device_id, result, backup_dir)
    if users_data and isinstance(users_data, list) and len(users_data) > 0:
        # 取第一个用户作为当前用户
        username = users_data[0].get("username", "")
    elif users_data and isinstance(users_data, dict):
        username = users_data.get("username", "")
        if not username and "users" in users_data:
            users = users_data["users"]
            if isinstance(users, list) and len(users) > 0:
                username = users[0].get("username", "")
    else:
        # 默认用户名
        username = "音乐爱好者"

    if not username:
        username = "音乐爱好者"

    logging.info(f"  → 设备中的用户名为: {username}")

    if username in final_msg:
        logging.info("✓ 测试通过 - 任务1完成：AI正确报告了用户名")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务1未完成：AI的回答'{final_msg}'中未包含正确的用户名'{username}'")
        return False


if __name__ == "__main__":
    print(check_username_is_reported())
