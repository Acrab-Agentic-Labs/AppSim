"""
任务15：点击当前播放的歌曲，查看歌曲详情
难度：中
"""

import logging
import sys
from verification_functions import read_json_from_device

def check_view_song_detail(result=None, device_id=None, backup_dir=None):
    """
    任务15: 验证是否查看了歌曲详情
    - 从 playback_state.json 获取当前歌曲ID
    - 检查 app_state.json 中 currentPage 是否为 'song_detail'
    - 检查 app_state.json 中 currentSongId 是否与当前播放的歌曲ID匹配
    """
    # 首先获取当前播放的歌曲ID
    playback_data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    if not playback_data or not playback_data.get("currentSong") or not playback_data["currentSong"].get("songId"):
        logging.error("✗ 测试失败 - 任务15未完成：无法从设备状态确定当前播放的歌曲ID")
        return False
    current_song_id = playback_data["currentSong"]["songId"]
    logging.info(f"  → 当前播放的歌曲ID为: {current_song_id}")

    # 然后检查App状态
    app_state_data = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state_data:
        logging.error("✗ 测试失败 - 任务15未完成：无法从设备读取App状态")
        return False

    current_page = app_state_data.get("currentPage")
    page_song_id = app_state_data.get("currentSongId")

    if current_page == "song_detail" and page_song_id == current_song_id:
        logging.info(f"✓ 测试通过 - 任务15完成：已进入歌曲'{current_song_id}'的详情页面")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务15未完成：页面状态不正确。期望页面: 'song_detail', 实际: '{current_page}'。期望SongID: '{current_song_id}', 实际: '{page_song_id}'")
        return False

if __name__ == "__main__":

    print(check_view_song_detail())
