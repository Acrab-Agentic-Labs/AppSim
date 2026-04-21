"""
任务33：数一下“我喜欢的音乐”里有几首歌曲
难度：中
类型：信息检索类
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device

def check_favorite_song_count(result=None, device_id=None, backup_dir=None):
    """
    任务33: 核实“我喜欢的音乐”歌单的歌曲数
    - 从AI回答中解析出歌曲数
    - 从设备读取user_favorites.json计算实际歌曲数
    - 对比两者是否一致
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务33未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务33未完成：final_message格式错误: {final_msg}")
        return False

    # 1. 从AI回答中解析出数字
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"✗ 测试失败 - 任务33未完成：未能在AI的回答中找到任何数字: '{final_msg}'")
        return False
    agent_count = int(numbers[0])
    logging.info(f"  → AI报告的歌曲数为: {agent_count}")

    # 2. 从设备读取真实数据
    favorites_data = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites_data or "favoriteSongs" not in favorites_data or not isinstance(favorites_data.get("favoriteSongs"), list):
        logging.error("✗ 测试失败 - 任务33未完成：无法从设备读取收藏数据或'favoriteSongs'字段格式不正确")
        return False

    # 3. 计算真实值
    device_count = len(favorites_data["favoriteSongs"])
    logging.info(f"  → 设备中的实际收藏歌曲数为: {device_count}")

    # 4. 对比验证
    if agent_count == device_count:
        logging.info("✓ 测试通过 - 任务33完成：AI报告的歌曲数与设备实际收藏数一致")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务33未完成：AI报告的歌曲数({agent_count})与设备实际收藏数({device_count})不符")
        return False

if __name__ == "__main__":

    print(check_favorite_song_count())
