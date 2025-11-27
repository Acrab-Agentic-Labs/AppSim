"""
任务8：收藏当前歌曲
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_song_is_favorited(result=None, device_id=None, backup_dir=None):
    """
    任务8: 验证当前歌曲是否被收藏
    - 从 playback_state.json 获取当前歌曲ID
    - 检查该ID是否存在于 user_favorites.json 的 favoriteSongs 列表中
    """
    # 首先获取当前播放的歌曲ID
    playback_data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    if not playback_data or not playback_data.get("currentSong") or not playback_data["currentSong"].get("songId"):
        logging.error("✗ 测试失败 - 任务8未完成：无法从设备状态确定当前播放的歌曲ID")
        return False
    current_song_id = playback_data["currentSong"]["songId"]
    logging.info(f"  → 当前歌曲ID为: {current_song_id}")

    # 然后检查收藏列表
    favorites_data = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites_data or "favoriteSongs" not in favorites_data or not isinstance(favorites_data.get("favoriteSongs"), list):
        logging.error("✗ 测试失败 - 任务8未完成：无法从设备读取收藏列表或数据格式不正确")
        return False

    song_ids = [song.get("songId") for song in favorites_data["favoriteSongs"]]
    if current_song_id in song_ids:
        logging.info(f"✓ 测试通过 - 任务8完成：歌曲 {current_song_id} 已成功收藏")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务8未完成：歌曲 {current_song_id} 未在收藏列表中找到")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务8：收藏当前歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放页面，确保有歌曲正在播放")
    print("  2. 点击收藏按钮（通常是爱心图标）")
    print("\n🔍 开始验证...")

    success = check_song_is_favorited()

    print(f"\n任务8验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
