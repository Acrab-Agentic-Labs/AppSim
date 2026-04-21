"""
任务1：进入‘我的’页面中‘我喜欢的音乐’这个歌单
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_enter_favorite_playlist(result=None, device_id=None, backup_dir=None):
    """
    任务1: 验证是否进入'我喜欢的音乐'歌单
    - 检查 user_playlists.json 中 currentViewingPlaylist 是否为 "my_favorites"
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)

    if data and data.get("currentViewingPlaylist") == "my_favorites":
        logging.info("✓ 测试通过 - 任务1完成：成功进入'我喜欢的音乐'歌单")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务1未完成：未能进入'我喜欢的音乐'歌单。检查到的页面是: {data.get('currentViewingPlaylist') if data else 'N/A'}")
        return False

if __name__ == "__main__":
    # 实际验证依赖于从设备读取的文件，若文件不存在则会失败
    print(check_enter_favorite_playlist())
