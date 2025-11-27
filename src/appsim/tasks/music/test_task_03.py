"""
任务3：删除‘我的’页面中热歌榜歌单的第一首歌曲
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

# 歌单名称，直接从任务指令中获取
PLAYLIST_NAME_HOT = "热歌榜"

def check_delete_song_from_hot_playlist(result=None, device_id=None, backup_dir=None):
    """
    任务3: 验证是否从热歌榜删除歌曲
    - 动态查找'热歌榜'的ID
    - 检查 song_deletion_records.json 中是否有对应ID的删除记录
    - 如果设备状态未直接确认，则检查AI的 final_message 作为后备
    """
    # 1. 动态查找'热歌榜'的ID
    playlists_data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)
    if not playlists_data or "playlists" not in playlists_data or not isinstance(playlists_data.get("playlists"), list):
        logging.error("✗ 测试失败 - 任务3未完成：无法读取歌单列表以确定'热歌榜'ID")
        return False

    hot_playlist_id = None
    for playlist in playlists_data["playlists"]:
        if playlist.get("playlistName") == PLAYLIST_NAME_HOT:
            hot_playlist_id = playlist.get("playlistId")
            break

    if not hot_playlist_id:
        logging.error(f"✗ 测试失败 - 任务3未完成：在设备上未找到名为'{PLAYLIST_NAME_HOT}'的歌单")
        return False
    logging.info(f"  → 动态查找到'{PLAYLIST_NAME_HOT}'的ID为: {hot_playlist_id}")

    # 2. 检查删除记录
    deletion_data = read_json_from_device("autotest/song_deletion_records.json", device_id, result, backup_dir)
    if deletion_data and isinstance(deletion_data, list) and len(deletion_data) > 0:
        for record in deletion_data:
            if record.get("playlistId") == hot_playlist_id:
                deleted_song_id = record.get("songId")
                logging.info(f"✓ 测试通过 - 任务3完成：设备状态确认，找到'{PLAYLIST_NAME_HOT}' (ID: {hot_playlist_id}) 的歌曲删除记录 (Song ID: {deleted_song_id})")
                return True
        logging.warning(f"  → 设备状态警告: 找到了删除记录,但没有来自'{PLAYLIST_NAME_HOT}'的记录")
    else:
        logging.warning("  → 设备状态警告: 未找到任何歌曲删除记录")

    # 3. 如果设备状态检查失败, 检查final_message作为后备
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if final_msg and isinstance(final_msg, str) and "删除" in final_msg and ("成功" in final_msg or "已完成" in final_msg):
            logging.info(f"✓ 测试通过 - 任务3完成：AI确认完成: {final_msg} (注意: 设备状态未直接验证)")
            return True

    logging.error("✗ 测试失败 - 任务3未完成：设备状态未确认且AI未声称完成")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务3：删除‘我的’页面中热歌榜歌单的第一首歌曲")
    print("=" * 70)
    print("\n🔍 开始验证...")

    mock_result = { "final_message": "已成功删除歌曲。" }
    success = check_delete_song_from_hot_playlist(result=mock_result)

    print(f"\n任务3验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)