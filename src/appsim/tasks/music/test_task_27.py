"""
任务27：更改"我喜欢的音乐"的排序顺序
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

TARGET_PLAYLIST_ID = "my_favorites"
TARGET_PLAYLIST_NAME = "我喜欢的音乐"

def check_playlist_sort_order_is_changed(result=None, device_id=None, backup_dir=None):
    """
    任务27: 验证"我喜欢的音乐"歌单的排序顺序是否已更改
    - 检查 user_playlists.json 中"我喜欢的音乐"歌单的 sortOrder 字段
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)

    if not data or not data.get("playlists"):
        logging.error("✗ 测试失败 - 任务27未完成：无法获取歌单信息")
        return False

    for playlist in data["playlists"]:
        pid = playlist.get("playlistId", "")
        pname = playlist.get("playlistName", "")
        if pid == TARGET_PLAYLIST_ID or TARGET_PLAYLIST_NAME in pname:
            sort_order = playlist.get("sortOrder", "default")
            if sort_order != "default":
                logging.info(f"✓ 测试通过 - 任务27完成：'{TARGET_PLAYLIST_NAME}'的排序顺序已更改为 '{sort_order}'")
                return True
            else:
                logging.error(f"✗ 测试失败 - 任务27未完成：'{TARGET_PLAYLIST_NAME}'的排序顺序仍为默认值")
                return False

    # 兼容：如果通过currentViewingPlaylist判断
    current_playlist_id = data.get("currentViewingPlaylist")
    if current_playlist_id:
        for playlist in data["playlists"]:
            if playlist.get("playlistId") == current_playlist_id:
                sort_order = playlist.get("sortOrder", "default")
                if sort_order != "default":
                    logging.info(f"✓ 测试通过 - 任务27完成：歌单排序顺序已更改为 '{sort_order}'")
                    return True

    logging.error(f"✗ 测试失败 - 任务27未完成：未找到'{TARGET_PLAYLIST_NAME}'歌单或排序未更改")
    return False

if __name__ == "__main__":

    print(check_playlist_sort_order_is_changed())
