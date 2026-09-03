"""
任务11：播放"每日推荐"中的第一首歌曲
难度：中
"""

import logging
import sys
from .verification_functions import is_daily_recommend_context, is_daily_recommend_song, is_in_daily_recommend_context, read_json_from_device

def _is_first_daily_song(current_song):
    source_detail = str(current_song.get("sourceDetail", ""))
    if any(marker in source_detail for marker in ["第1首", "第一首", "第 1 首"]):
        return True

    index_keys = ["index", "position", "queueIndex", "sourceIndex", "sourcePosition"]
    for key in index_keys:
        value = current_song.get(key)
        if value in (0, 1, "0", "1"):
            return True

    return False


def verify_first_daily_recommendation_played(result=None, device_id=None, backup_dir=None):
    """
    任务11: 验证是否播放了"每日推荐"的第一首歌
    - 检查 playback_state.json 中 currentSong 是否来自每日推荐
    - 检查 currentSong 中是否存在第一首歌曲证据
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    current_song = data.get("currentSong") if data else None
    playlists_data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)
    is_daily_song = current_song and (
        is_daily_recommend_song(current_song)
        or is_in_daily_recommend_context(data)
        or is_daily_recommend_context(playlists_data)
    )
    is_first_song = current_song and _is_first_daily_song(current_song)

    if is_daily_song and is_first_song:
        logging.info("✓ 测试通过 - 任务11完成：正在播放每日推荐的第一首歌")
        return True
    else:
        current_song_info = current_song if current_song else "N/A"
        logging.error(f"✗ 测试失败 - 任务11未完成：未检测到正在播放每日推荐的第一首歌。当前歌曲信息: {current_song_info}")
        return False

if __name__ == "__main__":

    print(verify_first_daily_recommendation_played())
