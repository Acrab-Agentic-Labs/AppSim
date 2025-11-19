"""
任务20：在推荐歌单中随机选择一个歌单并收藏
难度：中

人工操作步骤：
  1. 进入推荐
  2. 找到推荐歌单
  3. 点击收藏

验证标准：
调用task_20_check_collect_playlist函数进行验证

参数：playlist_id（歌单ID），默认自动检测最新收藏
"""

import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .verification_functions import read_json_from_device, task_20_check_collect_playlist


def test20(playlist_id=None, result=None, device_id=None):
    # 如果没有指定playlist_id，自动从collected_items.json获取最新收藏的歌单
    if playlist_id is None:
        collected_data = read_json_from_device("autotest/collected_items.json", device_id=device_id, result=result)

        if collected_data and "collectedPlaylists" in collected_data and collected_data["collectedPlaylists"]:
            # 获取最后一个（最新）收藏的歌单
            latest_playlist = collected_data["collectedPlaylists"][-1]
            playlist_id = latest_playlist.get("playlistId")
        else:
            logging.debug("✗ 错误：无法检测到已收藏的歌单")
            return False

    result1 = task_20_check_collect_playlist(playlist_id, device_id=device_id, result=result)

    if result1:
        logging.debug(f"✓ 测试通过 - 歌单 {playlist_id} 已成功收藏")
        return True
    else:
        logging.debug(f"✗ 测试失败 - 歌单 {playlist_id} 未在收藏列表中")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务20：在推荐歌单中随机选择一个歌单并收藏")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入推荐")
    print("  2. 找到推荐歌单")
    print("  3. 点击收藏")

    # 可以通过命令行参数传入playlist_id
    # 用法1：python test_task_20.py          # 自动检测最新收藏
    # 用法2：python test_task_20.py playlist_002  # 手动指定歌单ID
    playlist_id = sys.argv[1] if len(sys.argv) > 1 else None
    success = test20(playlist_id=playlist_id)

    print(f"任务20验证结果: {success}")
    sys.exit(0 if success else 1)
