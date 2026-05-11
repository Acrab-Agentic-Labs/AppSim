"""
任务20：在推荐歌单中收藏歌单"怀旧金曲"
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

TARGET_PLAYLIST_NAME = "怀旧金曲"
TARGET_PLAYLIST_ID = "playlist_006"

def check_playlist_is_collected(result=None, device_id=None, backup_dir=None):
    """
    任务20: 验证"怀旧金曲"歌单是否被收藏
    - 检查 collected_items.json 中是否包含"怀旧金曲"歌单
    """
    collected_data = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir)
    if not collected_data:
        logging.error("✗ 测试失败 - 任务20未完成：无法从设备读取收藏列表")
        return False

    # 支持两种数据结构
    collected_playlists = collected_data.get("collectedPlaylists", []) or collected_data.get("playlists", [])
    if not isinstance(collected_playlists, list):
        logging.error("✗ 测试失败 - 任务20未完成：收藏列表数据格式不正确")
        return False

    for p in collected_playlists:
        pid = p.get("playlistId", "")
        pname = p.get("playlistName", "") or p.get("name", "")
        if pid == TARGET_PLAYLIST_ID or TARGET_PLAYLIST_NAME in pname:
            logging.info(f"✓ 测试通过 - 任务20完成：歌单'{TARGET_PLAYLIST_NAME}'已成功收藏")
            return True

    logging.error(f"✗ 测试失败 - 任务20未完成：歌单'{TARGET_PLAYLIST_NAME}'未在收藏列表中找到")
    return False

if __name__ == "__main__":

    print(check_playlist_is_collected())
