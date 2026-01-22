"""
任务36：数一下我的粉丝数目
难度：中
类型：信息检索类
"""

import logging
import sys
import re
from verification_functions import read_json_from_device

def check_fan_count(result=None, device_id=None, backup_dir=None):
    """
    任务36: 核实我的粉丝数目
    - 从AI回答解析出数目
    - 从设备读取fan_items.json获取真实数目
    - 对比两者是否一致
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务36未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务36未完成：final_message格式错误: {final_msg}")
        return False

    # 1. 从AI回答中解析出数字
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"✗ 测试失败 - 任务36未完成：未能在AI的回答中找到任何数字: '{final_msg}'")
        return False
    agent_count = int(numbers[0])
    logging.info(f"  → AI报告的粉丝数为: {agent_count}")

    # 2. 从设备读取真实数据
    fan_items_data = read_json_from_device("autotest/fan_items.json", device_id, result, backup_dir)
    if not isinstance(fan_items_data, list):
        logging.error("✗ 测试失败 - 任务36未完成：无法从设备读取粉丝数据或数据格式不正确 (应为列表)")
        return False

    # 3. 获取真实值
    device_count = len(fan_items_data)
    logging.info(f"  → 设备中的实际粉丝数为: {device_count}")

    # 4. 对比验证
    if agent_count == device_count:
        logging.info("✓ 测试通过 - 任务36完成：AI报告的粉丝数与设备实际情况一致")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务36未完成：AI报告的粉丝数({agent_count})与设备实际情况({device_count})不符")
        return False

if __name__ == "__main__":

    print(check_fan_count())
