"""
任务23：取消收藏第一首歌曲
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_song_is_unfavorited(result=None, device_id=None, backup_dir=None):
    """
    任务23: 验证歌曲是否被取消收藏
    - 检查 user_favorites.json 中 recentUnfavorited 字段是否存在且包含歌曲ID
    - 这是一个简化的验证，只检查最近有取消收藏的行为发生。
    """
    data = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)

    if data and "recentUnfavorited" in data and data["recentUnfavorited"]:
        song_id = data["recentUnfavorited"]
        logging.info(f"✓ 测试通过 - 任务23完成：检测到最近有取消收藏行为，歌曲ID: {song_id}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务23未完成：未在设备状态中检测到取消收藏的记录")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务23：取消收藏第一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入'我喜欢的音乐'歌单")
    print("  2. 点击歌曲后的菜单按钮")
    print("  3. 选择'取消收藏'或类似选项")
    print("  (或者进入播放页面，再次点击爱心按钮取消收藏)")
    print("\n🔍 开始验证...")

    success = check_song_is_unfavorited()

    print(f"\n任务23验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
