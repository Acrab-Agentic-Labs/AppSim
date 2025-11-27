"""
任务37：数一下“热歌榜”里有多少首歌曲
难度：中
类型：信息检索类
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device

PLAYLIST_NAME_HOT = "热歌榜"

def check_hot_rank_song_count(result=None, device_id=None, backup_dir=None):
    """
    任务37: 核实热歌榜的歌曲数目
    - 从AI回答解析数目
    - 从设备读取user_playlists.json找到热歌榜并获取数目
    - 对比两者是否一致
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务37未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务37未完成：final_message格式错误: {final_msg}")
        return False

    # 1. 从AI回答中解析出数字
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"✗ 测试失败 - 任务37未完成：未能在AI的回答中找到任何数字: '{final_msg}'")
        return False
    agent_count = int(numbers[0])
    logging.info(f"  → AI报告的歌曲数为: {agent_count}")

    # 2. 从设备读取真实数据
    playlists_data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)
    if not playlists_data or "playlists" not in playlists_data or not isinstance(playlists_data.get("playlists"), list):
        logging.error("✗ 测试失败 - 任务37未完成：无法从设备读取歌单数据或'playlists'字段格式不正确")
        return False

    # 3. 计算真实值
    device_count = 0
    found_playlist = False
    for playlist in playlists_data["playlists"]:
        if playlist.get("playlistName") == PLAYLIST_NAME_HOT:
            device_count = playlist.get("songCount", 0)
            found_playlist = True
            break
    if not found_playlist:
        logging.error(f"✗ 测试失败 - 任务37未完成：设备数据中未找到名为'{PLAYLIST_NAME_HOT}'的歌单")
        return False
    logging.info(f"  → 设备中'{PLAYLIST_NAME_HOT}'的实际歌曲数为: {device_count}")

    # 4. 对比验证
    if agent_count == device_count:
        logging.info("✓ 测试通过 - 任务37完成：AI报告的歌曲数与设备实际情况一致")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务37未完成：AI报告的歌曲数({agent_count})与设备实际情况({device_count})不符")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务37：数一下“热歌榜”里有多少首歌曲")
    print("=" * 70)
    print("\n🔍 开始验证...")

    mock_result = { "final_message": "热歌榜里一共有 100 首歌。" }
    success = check_hot_rank_song_count(result=mock_result)

    print(f"\n任务37验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)