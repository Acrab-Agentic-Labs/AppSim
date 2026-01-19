"""
任务18：进入排行榜的新歌榜，告诉我第一首歌叫什么
难度：中
类型：信息检索类
"""

import logging
import sys
from .verification_functions import read_json_from_device

RANK_NAME_NEW_SONGS = "新歌榜"

def check_first_song_name_is_reported(result=None, device_id=None, backup_dir=None):
    """
    任务18: 验证AI是否返回了新歌榜第一首歌的名称
    - 从AI的 final_message 中提取歌曲名称
    - 从 playlists.json 读取新歌榜的真实第一首歌名
    - 对比两者是否一致
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务18未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务18未完成：final_message格式错误: {final_msg}")
        return False

    # 1. 从设备读取真实数据
    rankings_data = read_json_from_device("autotest/playlists.json", device_id, result, backup_dir)
    if not rankings_data or "charts" not in rankings_data or not isinstance(rankings_data.get("charts"), list):
        logging.error("✗ 测试失败 - 任务18未完成：无法从设备读取排行榜数据或数据格式不正确")
        return False

    # 2. 查找新歌榜并获取第一首歌名
    first_song_name = None
    for chart in rankings_data["charts"]:
        if chart.get("chartName") == RANK_NAME_NEW_SONGS:
            if chart.get("songs") and len(chart["songs"]) > 0:
                first_song_name = chart["songs"][0].get("songName")
                break
    
    if not first_song_name:
        logging.error(f"✗ 测试失败 - 任务18未完成：在设备数据中未找到'{RANK_NAME_NEW_SONGS}'或该榜单为空")
        return False
    logging.info(f"  → 设备中'{RANK_NAME_NEW_SONGS}'的第一首歌是: '{first_song_name}'")

    # 3. 检查AI的回答
    if first_song_name in final_msg:
        logging.info(f"✓ 测试通过 - 任务18完成：AI正确返回了第一首歌的名称: '{final_msg}'")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务18未完成：AI返回错误。期望包含'{first_song_name}', 实际返回: '{final_msg}'")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务18：进入排行榜的新歌榜，告诉我第一首歌叫什么")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP，进入'排行榜'页面")
    print("  2. 找到并点击'新歌榜'")
    print("  3. 查看第一首歌的名称并返回")
    print("\n🔍 开始验证...")

    # 模拟AI返回正确歌名的情况
    mock_result = {
        "final_message": "新歌榜的第一首歌是《星辰大海》。"
    }

    success = check_first_song_name_is_reported(result=mock_result)

    print(f"\n任务18验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
