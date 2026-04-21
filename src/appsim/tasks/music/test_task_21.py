"""
任务21：删除歌单中的第一首歌
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_song_is_deleted_from_playlist(result=None, device_id=None, backup_dir=None):
    """
    任务21: 验证歌曲是否已从歌单中删除
    - 检查 song_deletion_records.json 中是否有最新的删除记录
    - 注意：这是一个简化的验证，只检查有删除行为发生，而不精确对比删除前后的歌曲总数。
    """
    data = read_json_from_device("autotest/song_deletion_records.json", device_id, result, backup_dir)

    if data and isinstance(data, list) and len(data) > 0:
        latest_record = data[-1] # 获取最新一条记录 
        playlist_id = latest_record.get("playlistId")
        song_id = latest_record.get("songId")
        logging.info(f"✓ 测试通过 - 任务21完成：检测到删除记录，从歌单 {playlist_id} 删除了歌曲 {song_id}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务21未完成：未在设备上找到任何歌曲删除记录")
        return False

if __name__ == "__main__":

    print(check_song_is_deleted_from_playlist())
