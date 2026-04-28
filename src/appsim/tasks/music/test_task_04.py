"""
任务4：播放每日推荐的歌曲
难度：低
"""

import logging
import sys
from .verification_functions import is_daily_recommend_context, is_daily_recommend_song, is_in_daily_recommend_context, read_json_from_device

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

    # 检查歌曲来源或当前查看的页面/歌单上下文
    playlists_data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)
    is_daily_context = is_in_daily_recommend_context(data) or is_daily_recommend_context(playlists_data)
    if not is_daily_recommend_song(current_song) and not is_daily_context:
        logging.error(f"✗ 测试失败 - 任务4未完成：播放来源不是每日推荐。当前歌曲信息: {current_song}")
        logging.info(f"  当前播放状态: {data}")
        logging.info(f"  当前歌单状态: {playlists_data}")
        logging.info("  提示: 需要从'每日推荐'页面点击歌曲播放")
        return False

    # 所有检查通过
    song_name = current_song.get("songName", "未知")
    logging.info(f"✓ 测试通过 - 任务4完成：正在播放每日推荐的歌曲 '{song_name}'")
    return True

if __name__ == "__main__":

    print(check_is_playing())
