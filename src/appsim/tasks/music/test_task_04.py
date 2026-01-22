"""
任务4：播放每日推荐的歌曲
难度：低
"""

import logging
import sys
from verification_functions import read_json_from_device

def check_is_playing(result=None, device_id=None, backup_dir=None):
    """
    任务4: 验证是否正在播放每日推荐的歌曲
    - 检查 playback_state.json 中 isPlaying 是否为 true
    - 检查 currentSong.source 是否为 "daily_recommend"
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if not data:
        logging.error("✗ 测试失败 - 任务4未完成：无法读取播放状态数据")
        return False

    # 检查是否正在播放
    is_playing = data.get("isPlaying")
    if not is_playing:
        logging.error(f"✗ 测试失败 - 任务4未完成：歌曲未在播放。isPlaying = {is_playing}")
        return False

    # 检查歌曲来源
    current_song = data.get("currentSong")
    if not current_song:
        logging.error("✗ 测试失败 - 任务4未完成：没有当前播放的歌曲信息")
        return False

    source = current_song.get("source", "")
    if source != "daily_recommend":
        logging.error(f"✗ 测试失败 - 任务4未完成：播放的歌曲不是来自每日推荐。当前来源: '{source}'")
        logging.info(f"  提示: 请从'每日推荐'页面点击歌曲播放")
        return False

    # 所有检查通过
    song_name = current_song.get("songName", "未知")
    logging.info(f"✓ 测试通过 - 任务4完成：正在播放每日推荐的歌曲 '{song_name}'")
    return True

if __name__ == "__main__":

    print(check_is_playing())
