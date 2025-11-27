"""
任务35：数一下首页“每日推荐”中有多少首歌曲
难度：中
类型：信息检索类

人工操作步骤：
  1. 打开音乐APP
  2. 进入首页（推荐页面）
  3. 找到"每日推荐"板块
  4. 查看并返回该板块中的歌曲总数

验证标准：
调用task_35_check_daily_recommendation_song_count函数进行验证
AI返回的歌曲数必须与设备文件中"每日推荐"歌单的实际歌曲数相符
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device

# 假设首页"每日推荐"板块的数据来源是 user_playlists.json 中的 "每日推荐" 歌单
PLAYLIST_NAME_DAILY_RECOMMEND = "每日推荐"


def task_35_check_daily_recommendation_song_count(result=None, device_id=None, backup_dir=None):
    """
    任务35: 核实首页“每日推荐”的歌曲数目
    验证: 1. 从AI回答解析数目. 2. 从设备读取user_playlists.json找到“每日推荐”歌单的数目. 3. 对比.
    """
    if not result or "final_message" not in result:
        logging.error("  → AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"  → final_message格式错误: {final_msg}")
        return False

    # 1. 从AI回答中解析出数字
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"  → 未能在AI的回答中找到任何数字: {final_msg}")
        return False
    agent_count = int(numbers[0])
    logging.info(f"  → AI报告的首页‘每日推荐’歌曲数为: {agent_count}")

    # 2. 从设备读取真实数据
    playlists_data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)
    if not playlists_data or "playlists" not in playlists_data or not isinstance(playlists_data.get("playlists"), list):
        logging.error("  → 无法从设备读取歌单数据或'playlists'字段格式不正确")
        return False

    # 3. 计算真实值
    device_count = 0
    found_playlist = False
    for playlist in playlists_data["playlists"]:
        if playlist.get("playlistName") == PLAYLIST_NAME_DAILY_RECOMMEND:
            device_count = playlist.get("songCount", 0)
            found_playlist = True
            break
    if not found_playlist:
        logging.error(f"  → 设备数据中未找到名为'{PLAYLIST_NAME_DAILY_RECOMMEND}'的歌单")
        return False
    logging.info(f"  → 设备中歌单'{PLAYLIST_NAME_DAILY_RECOMMEND}'的实际歌曲数为: {device_count}")

    # 4. 对比验证
    if agent_count == device_count:
        logging.info("  → 验证成功: AI报告的歌曲数与设备实际情况一致")
        return True
    else:
        logging.error(f"  → 验证失败: AI报告的歌曲数({agent_count})与设备实际情况({device_count})不符")
        return False


def test(result=None, device_id=None, backup_dir=None):
    """
    执行任务35的测试
    """
    if task_35_check_daily_recommendation_song_count(result, device_id, backup_dir):
        logging.info("✓ 测试通过 - 任务35完成")
        return True
    else:
        logging.error("✗ 测试失败 - 任务35未完成")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务35：数一下首页“每日推荐”中有多少首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入首页（推荐页面）")
    print("  3. 找到'每日推荐'板块")
    print("  4. 查看并返回该板块中的歌曲总数")
    print("\n🔍 开始验证...")

    mock_result = { "final_message": "首页每日推荐有 30 首歌曲。" }
    success = test(result=mock_result)

    print(f"\n任务35验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)