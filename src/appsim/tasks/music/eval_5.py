"""
任务5：暂停播放当前的歌曲
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def verify_current_song_paused(result=None, device_id=None, backup_dir=None):
    """
    任务5: 验证歌曲是否已暂停
    - 检查 playback_state.json 中 isPlaying 是否为 false
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and data.get("isPlaying") == False:
        logging.info("✓ 测试通过 - 任务5完成：歌曲已暂停")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务5未完成：歌曲未暂停。检查到的状态是: {data.get('isPlaying') if data else 'N/A'}")
        return False

if __name__ == "__main__":

    print(verify_current_song_paused())
