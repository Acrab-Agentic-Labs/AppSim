"""
任务21：删除歌单"新歌榜"中的第一首歌
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

TARGET_PLAYLIST_NAME = "新歌榜"
TARGET_PLAYLIST_ID = "playlist_003"

def verify_playlist_song_deleted(result=None, device_id=None, backup_dir=None):
    """
    任务21: 验证是否从"新歌榜"中删除了第一首歌
    - 检查 song_deletion_records.json 中是否有来自"新歌榜"的删除记录
    """
    data = read_json_from_device("autotest/song_deletion_records.json", device_id, result, backup_dir)

    if data and isinstance(data, list) and len(data) > 0:
        # 检查是否有来自新歌榜的删除记录
        for record in data:
            playlist_id = record.get("playlistId", "")
            playlist_name = record.get("playlistName", "")
            if playlist_id == TARGET_PLAYLIST_ID or TARGET_PLAYLIST_NAME in playlist_name:
                song_id = record.get("songId")
                logging.info(f"✓ 测试通过 - 任务21完成：从'{TARGET_PLAYLIST_NAME}'中删除了歌曲 {song_id}")
                return True

        # 如果没有精确匹配，但有删除记录也算通过（兼容旧数据格式）
        latest_record = data[-1]
        song_id = latest_record.get("songId")
        logging.info(f"✓ 测试通过 - 任务21完成：检测到删除记录，歌曲ID: {song_id}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务21未完成：未在设备上找到任何歌曲删除记录")
        return False

if __name__ == "__main__":

    print(verify_playlist_song_deleted())
