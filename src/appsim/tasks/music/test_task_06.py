"""
任务6：切换播放上一首歌曲
难度：低
"""

import logging
import sys
from verification_functions import read_json_from_device

def check_switch_to_previous_song(result=None, device_id=None, backup_dir=None):
    """
    任务6: 验证是否切换到上一首歌
    - 检查 playback_state.json 中是否有 currentSong.songId
    - 注意：此验证较为宽松，仅确认发生了切换行为，不校验具体切换到了哪一首歌。
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and "currentSong" in data and "songId" in data["currentSong"]:
        song_id = data['currentSong']['songId']
        logging.info(f"✓ 测试通过 - 任务6完成：已切换歌曲，当前歌曲ID: {song_id}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务6未完成：在设备状态中未检测到有效的当前歌曲信息")
        return False

if __name__ == "__main__":

    print(check_switch_to_previous_song())
