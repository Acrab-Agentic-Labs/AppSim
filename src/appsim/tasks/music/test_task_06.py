"""
任务6：切换播放上一首歌曲
难度：低
"""

import logging
import sys
from .verification_functions import has_previous_action, read_json_from_device

def check_switch_to_previous_song(result=None, device_id=None, backup_dir=None):
    """
    任务6: 验证是否切换到上一首歌
    - 检查 playback_state.json 或 play_records.json 中是否有上一首动作证据
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and has_previous_action(data):
        current_song = data.get("currentSong", {})
        song_id = current_song.get("songId", "未知")
        logging.info(f"✓ 测试通过 - 任务6完成：检测到上一首动作，当前歌曲ID: {song_id}")
        return True

    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir=backup_dir)
    if isinstance(play_records, list) and any(has_previous_action(record) for record in play_records[-3:]):
        logging.info("✓ 测试通过 - 任务6完成：播放记录中检测到上一首动作")
        return True

    logging.error("✗ 测试失败 - 任务6未完成：未检测到切换上一首歌曲的动作记录")
    return False

if __name__ == "__main__":

    print(check_switch_to_previous_song())
