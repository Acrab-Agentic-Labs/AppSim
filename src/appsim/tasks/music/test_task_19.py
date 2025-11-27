"""
任务19：在排行榜中打开一个榜单并播放第一首歌曲
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_play_from_rank_list(result=None, device_id=None, backup_dir=None):
    """
    任务19: 验证是否播放了排行榜的歌曲
    - 检查 playback_state.json 中 currentSong.source 是否包含 'rank' 或 '榜单'
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and "currentSong" in data and data["currentSong"]:
        source = data["currentSong"].get("source", "")
        if "rank" in source or "榜单" in source:
            logging.info(f"✓ 测试通过 - 任务19完成：正在播放来自排行榜的歌曲 (source: {source})")
            return True

    source_info = data.get("currentSong", {}).get("source") if data and data.get("currentSong") else "N/A"
    logging.error(f"✗ 测试失败 - 任务19未完成：当前歌曲来源不正确。期望包含'rank'或'榜单', 实际: '{source_info}'")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务19：在排行榜中打开一个榜单并播放第一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP，进入'排行榜'页面")
    print("  2. 选择任意一个榜单")
    print("  3. 点击第一首歌曲进行播放")
    print("\n🔍 开始验证...")

    success = check_play_from_rank_list()

    print(f"\n任务19验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
