"""
任务34：计算我的歌单中“每日推荐”和“热歌榜”一共多少首歌曲
难度：高
类型：信息检索/计算类

人工操作步骤：
  1. 打开音乐APP，进入"我的"页面
  2. 查看"每日推荐"的歌曲数
  3. 查看"热歌榜"的歌曲数
  4. 将两个数字相加并返回总数

验证标准：
调用task_34_check_playlist_song_sum函数进行验证
AI返回的总数必须与设备文件中两个歌单的歌曲数之和相符
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device

# 歌单名称，直接从任务指令中获取
PLAYLIST_NAME_DAILY = "每日推荐"
PLAYLIST_NAME_HOT = "热歌榜"


def task_34_check_playlist_song_sum(result=None, device_id=None, backup_dir=None):
    """
    任务34: 核实每日推荐和热歌榜的歌曲总数
    验证: 1. 从AI回答中解析出总数. 2. 从设备读取user_playlists.json计算真实总数. 3. 对比.
    """
    if not result or "final_message" not in result:
        logging.error("  → AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"  → final_message格式错误: {final_msg}")
        return False

    # 1. 从AI回答中解析出数字 (通常总数会是最后一个数字)
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"  → 未能在AI的回答中找到任何数字: {final_msg}")
        return False
    agent_sum = int(numbers[-1])
    logging.info(f"  → AI报告的歌曲总数为: {agent_sum}")

    # 2. 从设备读取真实数据
    playlists_data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)
    if not playlists_data or "playlists" not in playlists_data or not isinstance(playlists_data.get("playlists"), list):
        logging.error("  → 无法从设备读取歌单数据或'playlists'字段格式不正确")
        return False

    # 3. 计算真实值 - 通过歌单名称查找
    count_daily = 0
    count_hot = 0
    found_daily = False
    found_hot = False

    for playlist in playlists_data["playlists"]:
        if playlist.get("playlistName") == PLAYLIST_NAME_DAILY:
            count_daily = playlist.get("songCount", 0)
            found_daily = True
        elif playlist.get("playlistName") == PLAYLIST_NAME_HOT:
            count_hot = playlist.get("songCount", 0)
            found_hot = True

    if not found_daily:
        logging.warning(f"  → 设备数据中未找到歌单: '{PLAYLIST_NAME_DAILY}'")
    if not found_hot:
        logging.warning(f"  → 设备数据中未找到歌单: '{PLAYLIST_NAME_HOT}'")

    device_sum = count_daily + count_hot
    logging.info(f"  → 设备中'{PLAYLIST_NAME_DAILY}'({count_daily}) + '{PLAYLIST_NAME_HOT}'({count_hot})的实际总数为: {device_sum}")

    # 4. 对比验证
    if agent_sum == device_sum:
        logging.info("  → 验证成功: AI报告的总数与设备实际总数一致")
        return True
    else:
        logging.error(f"  → 验证失败: AI报告的总数({agent_sum})与设备实际总数({device_sum})不符")
        return False


def test(result=None, device_id=None, backup_dir=None):
    """
    执行任务34的测试
    """
    if task_34_check_playlist_song_sum(result, device_id, backup_dir):
        logging.info("✓ 测试通过 - 任务34完成")
        return True
    else:
        logging.error("✗ 测试失败 - 任务34未完成")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务34：计算我的歌单中“每日推荐”和“热歌榜”一共多少首歌曲")
    print("=" * 70)
    print("\n🔍 开始验证...")

    mock_result = { "final_message": "这两个歌单总共有 88 首歌。" }
    success = test(result=mock_result)

    print(f"\n任务34验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)