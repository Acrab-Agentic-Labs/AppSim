"""
任务39：搜索歌手“周杰伦”，计算他的歌曲总数
难度：高
类型：信息检索/计算类

人工操作步骤：
  1. 打开音乐APP
  2. 搜索"周杰伦"
  3. 进入歌手主页
  4. 查看歌曲列表并获取总数
  5. 返回总数

验证标准：
调用task_39_check_artist_song_count函数进行验证
AI返回的歌曲总数必须与设备文件artist_details.json中该歌手的实际歌曲数相符 (假设存在此文件)
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device

# 假设周杰伦在测试环境中的歌手ID
ARTIST_ID_JAY_CHOU = "artist_001"


def task_39_check_artist_song_count(result=None, device_id=None, backup_dir=None):
    """
    任务39: 核实歌手'周杰伦'的歌曲总数
    验证: 1. 从AI回答解析总数. 2. 从设备读取artist_details.json获取真实总数. 3. 对比.
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
    agent_count = int(numbers[-1])  # 取最后一个数字作为总数
    logging.info(f"  → AI报告的歌曲总数为: {agent_count}")

    # 2. 从设备读取真实数据 (假设存在 artist_details.json)
    artist_data = read_json_from_device("autotest/artist_details.json", device_id, result, backup_dir)
    # 假设文件结构为 {"artistId": "...", "songs": [...]} 
    if (not artist_data
            or artist_data.get("artistId") != ARTIST_ID_JAY_CHOU
            or "songs" not in artist_data
            or not isinstance(artist_data.get("songs"), list)):
        logging.error(f"  → 无法从设备读取艺术家详情, 或当前艺术家不是{ARTIST_ID_JAY_CHOU}, 或数据格式不正确")
        return False

    # 3. 获取真实值
    device_count = len(artist_data["songs"])
    logging.info(f"  → 设备中该艺术家的实际歌曲数为: {device_count}")

    # 4. 对比验证
    if agent_count == device_count:
        logging.info("  → 验证成功: AI报告的歌曲总数与设备实际情况一致")
        return True
    else:
        logging.error(f"  → 验证失败: AI报告的歌曲总数({agent_count})与设备实际情况({device_count})不符")
        return False


def test(result=None, device_id=None, backup_dir=None):
    """
    执行任务39的测试
    """
    if task_39_check_artist_song_count(result, device_id, backup_dir):
        logging.info("✓ 测试通过 - 任务39完成")
        return True
    else:
        logging.error("✗ 测试失败 - 任务39未完成")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务39：搜索歌手“周杰伦”，计算他的歌曲总数")
    print("=" * 70)
    print("\n🔍 开始验证...")

    mock_result = { "final_message": "周杰伦的歌曲总数是 258 首。" }
    success = test(result=mock_result)

    print(f"\n任务39验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
