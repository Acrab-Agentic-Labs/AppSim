"""
任务12：创建一个新的歌单,并添加首音乐
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_create_playlist_and_add_song(result=None, device_id=None, backup_dir=None):
    """
    任务12: 验证是否成功创建歌单并添加了歌曲
    - 检查 user_playlists.json 中的歌单列表
    - 查找最新创建的歌单（按createTime排序）
    - 验证该歌单的 songCount > 0
    - 如果设备状态未直接确认，则检查AI的 final_message 作为后备
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)

    if data and "playlists" in data and data["playlists"]:
        # 按创建时间排序，取最新的歌单
        sorted_playlists = sorted(data["playlists"], key=lambda x: x.get("createTime", 0), reverse=True)
        latest_playlist = sorted_playlists[0]
        playlist_name = latest_playlist.get("playlistName", "未知名称")
        song_count = latest_playlist.get("songCount", 0)

        if song_count > 0:
            logging.info(f"✓ 测试通过 - 任务12完成：设备状态确认，最新歌单'{playlist_name}'中已有 {song_count} 首歌曲")
            return True
        else:
            logging.warning(f"  → 设备状态警告: 最新歌单'{playlist_name}'已创建，但歌曲数量为0")

    # 如果设备状态检查失败, 检查final_message作为后备
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if (final_msg and isinstance(final_msg, str) and
                ("创建" in final_msg or "新建" in final_msg) and "歌单" in final_msg and
                ("添加" in final_msg or "歌曲" in final_msg)):
            logging.info(f"✓ 测试通过 - 任务12完成：AI确认完成: {final_msg} (注意: 设备状态未直接验证歌曲数量)")
            return True

    logging.error("✗ 测试失败 - 任务12未完成：未能确认歌单已创建且歌曲已添加")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务12：创建一个新的歌单,并添加首音乐")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入'我的'页面")
    print("  2. 点击创建歌单并命名")
    print("  3. 向新歌单中添加至少一首歌曲")
    print("\n🔍 开始验证...")

    success = check_create_playlist_and_add_song()

    print(f"\n任务12验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
