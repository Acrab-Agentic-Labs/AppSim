"""
任务11：播放"每日推荐"中的第一首歌曲
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_play_first_daily_recommendation(result=None, device_id=None, backup_dir=None):
    """
    任务11: 验证是否播放了"每日推荐"的第一首歌
    - 检查 playback_state.json 中 currentSon
    g.source 是否为 "daily_recommend"
    - 检查 currentSong.sourceDetail 是否包含 "第1首"
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if (data and "currentSong" in data and
            data["currentSong"].get("source") == "daily_recommend" and
            "第1首" in data["currentSong"].get("sourceDetail", "")):
        logging.info("✓ 测试通过 - 任务11完成：正在播放每日推荐的第一首歌")
        return True
    else:
        current_song_info = data.get("currentSong") if data else "N/A"
        logging.error(f"✗ 测试失败 - 任务11未完成：未检测到正在播放每日推荐的第一首歌。当前歌曲信息: {current_song_info}")
        return False

if __name__ == "__main__":

    print(check_play_first_daily_recommendation())
