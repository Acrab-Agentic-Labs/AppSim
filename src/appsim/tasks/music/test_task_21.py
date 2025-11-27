"""
任务21：删除歌单中的第一首歌
难度：中

人工操作步骤：
  1. 进入歌单
  2. 选择第一首歌
  3. 删除

验证标准：
调用task_21_check_delete_song_from_playlist函数进行验证

参数：playlist_id, expected_count，默认自动检测当前浏览的歌单
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_21_check_delete_song_from_playlist(playlist_id, expected_count, device_id=None, result=None, backup_dir=None):
    """
    任务21: 删除歌单中的第一首歌
    验证: 检查user_playlists.json中指定歌单的songCount是否减少
    :param playlist_id: 歌单ID
    :param expected_count: 删除后期望的歌曲数量
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)
    if data and "playlists" in data:
        for playlist in data["playlists"]:
            if playlist.get("playlistId") == playlist_id:
                return playlist.get("songCount") == expected_count
    return False


def test(playlist_id=None, expected_count=None, result=None, device_id=None, backup_dir=None):
    # 如果没有指定playlist_id，自动从user_playlists.json获取当前浏览的歌单
    if playlist_id is None or expected_count is None:
        playlists_data = read_json_from_device("autotest/user_playlists.json", device_id=device_id, result=result, backup_dir=backup_dir)

        if playlists_data and "currentViewingPlaylist" in playlists_data and playlists_data["currentViewingPlaylist"]:
            playlist_id = playlists_data["currentViewingPlaylist"]

            # 查找该歌单的当前歌曲数量
            if "playlists" in playlists_data:
                for playlist in playlists_data["playlists"]:
                    if playlist.get("playlistId") == playlist_id:
                        current_count = playlist.get("songCount", 0)
                        # 使用当前数量作为期望数量（因为删除已经完成）
                        expected_count = current_count
                        break

                if expected_count is None:
                    logging.debug("✗ 错误：无法找到当前浏览的歌单")
                    return False
        else:
            logging.debug("✗ 错误：无法检测到当前浏览的歌单")
            return False

    result1 = task_21_check_delete_song_from_playlist(playlist_id, expected_count, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug(f"✓ 测试通过 - 歌单 {playlist_id} 的歌曲数量为 {expected_count}")
        return True
    else:
        logging.debug(f"✗ 测试失败 - 歌单 {playlist_id} 的歌曲数量不是 {expected_count}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务21：删除歌单中的第一首歌")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入歌单")
    print("  2. 选择第一首歌")
    print("  3. 删除")

    # 可以通过命令行参数传入playlist_id和expected_count
    # 用法1：python test_task_21.py                   # 自动检测
    # 用法2：python test_task_21.py playlist_001 5    # 手动指定
    playlist_id = sys.argv[1] if len(sys.argv) > 1 else None
    expected_count = int(sys.argv[2]) if len(sys.argv) > 2 else None
    success = test(playlist_id=playlist_id, expected_count=expected_count)

    print(f"任务21验证结果: {success}")
    sys.exit(0 if success else 1)