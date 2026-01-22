"""
任务20：在推荐歌单中随机选择一个歌单并收藏
难度：中
"""

import logging
import sys
from verification_functions import read_json_from_device

def check_playlist_is_collected(result=None, device_id=None, backup_dir=None):
    """
    任务20: 验证歌单是否被收藏
    - 从 app_state.json 获取当前查看的歌单ID
    - 检查该ID是否存在于 collected_items.json 的 collectedPlaylists 列表中
    """
    # 首先获取当前正在查看的歌单ID
    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state or not app_state.get("currentPlaylistId"):
        logging.error("✗ 测试失败 - 任务20未完成：无法从设备状态确定当前查看的歌单ID")
        return False
    current_playlist_id = app_state["currentPlaylistId"]
    logging.info(f"  → 当前查看的歌单ID为: {current_playlist_id}")

    # 然后检查收藏列表
    collected_data = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir)
    if not collected_data or "collectedPlaylists" not in collected_data or not isinstance(collected_data.get("collectedPlaylists"), list):
        logging.error("✗ 测试失败 - 任务20未完成：无法从设备读取收藏列表或数据格式不正确")
        return False

    playlist_ids = [p.get("playlistId") for p in collected_data["collectedPlaylists"]]
    if current_playlist_id in playlist_ids:
        logging.info(f"✓ 测试通过 - 任务20完成：歌单 {current_playlist_id} 已成功收藏")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务20未完成：歌单 {current_playlist_id} 未在收藏列表中找到")
        return False

if __name__ == "__main__":

    print(check_playlist_is_collected())
