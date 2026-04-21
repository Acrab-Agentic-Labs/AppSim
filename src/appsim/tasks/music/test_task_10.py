"""
任务10：随机进入'我的'中的一个歌单
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_enter_any_playlist(result=None, device_id=None, backup_dir=None):
    """
    任务10: 验证是否进入了任意一个歌单
    - 检查 user_playlists.json 中 currentViewingPlaylist 是否不为null
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)

    if data and data.get("currentViewingPlaylist") is not None:
        playlist_id = data.get("currentViewingPlaylist")
        logging.info(f"✓ 测试通过 - 任务10完成：已进入歌单，ID为 {playlist_id}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务10未完成：未进入任何歌单 (currentViewingPlaylist is null)")
        return False

if __name__ == "__main__":

    print(check_enter_any_playlist())
