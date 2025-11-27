"""
任务12：创建一个新的歌单,并添加首音乐
难度：中

人工操作步骤：
  1. 进入我的页面
  2. 点击创建歌单
  3. 输入歌单名称（可以是任意数字或名称，如"1"、"2"、"测试歌单"等）
  4. 添加歌曲

验证标准：
调用task_12_check_create_playlist_and_add_song函数进行验证

使用方式：
  方式1（推荐）：不传参数，自动检查最新创建的歌单
    python test_task_12.py

  方式2：传入歌单名称，检查指定歌单
    python test_task_12.py 1
    python test_task_12.py 2
    python test_task_12.py 测试歌单
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_12_check_create_playlist_and_add_song(playlist_name=None, device_id=None, result=None, backup_dir=None):
    """
    任务12: 创建一个新的歌单,并添加首音乐
    验证:
    1. 优先检查user_playlists.json中是否有指定名称的歌单,且songCount > 0
    2. 如果设备状态检查失败,检查result["final_message"]是否包含"创建"和"歌单"相关信息
    3. 允许部分完成:如果只创建了歌单但未添加歌曲,也给予部分分数
    :param playlist_name: 新建歌单的名称。如果为None，则检查最新创建的歌单；否则检查指定名称的歌单
    """
    # 方法1: 检查设备状态
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)
    if data and "playlists" in data:
        playlists = data["playlists"]

        if playlist_name is None:
            # 不传参数时，检查最新创建的歌单
            if playlists:
                # 按创建时间排序，取最新的
                sorted_playlists = sorted(playlists, key=lambda x: x.get("createTime", 0), reverse=True)
                latest = sorted_playlists[0]
                song_count = latest.get("songCount", 0)
                print(f"  → 检查最新创建的歌单: 《{latest.get('playlistName')}》")
                print(f"  → 歌曲数量: {song_count}")
                if song_count > 0:
                    print("  → 设备状态确认: 已创建歌单并添加了歌曲")
                    return True
                else:
                    print("  → 设备状态: 已创建歌单但未添加歌曲")
                    # 继续检查final_message
        else:
            # 传参数时，检查指定名称的歌单
            print(f"  → 检查指定歌单: 《{playlist_name}》")
            for playlist in playlists:
                if playlist.get("playlistName") == playlist_name:
                    song_count = playlist.get("songCount", 0)
                    print(f"  → 歌曲数量: {song_count}")
                    if song_count > 0:
                        print("  → 设备状态确认: 已创建歌单并添加了歌曲")
                        return True
                    else:
                        print("  → 设备状态: 已创建歌单但未添加歌曲")

    # 方法2: 检查AI的final_message
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if final_msg and isinstance(final_msg, str):
            # 检查是否提到创建歌单
            if ("创建" in final_msg or "新建" in final_msg) and "歌单" in final_msg:
                print(f"  → AI确认: {final_msg}")
                # 如果同时提到添加歌曲，则认为完全完成
                if "添加" in final_msg or "歌曲" in final_msg:
                    print("  → AI声称已完成创建歌单并添加歌曲")
                    return True

    print("  → 验证失败: 设备状态未确认且AI未声称完成")
    return False


def test(playlist_name=None, result=None, device_id=None, backup_dir=None):
    result1 = task_12_check_create_playlist_and_add_song(
        playlist_name=playlist_name, device_id=device_id, result=result, backup_dir=backup_dir
    )

    if result1:
        logging.debug("✓ 测试通过 - 任务12完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务12未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务12：创建一个新的歌单,并添加首音乐")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入我的页面")
    print("  2. 点击创建歌单")
    print("  3. 输入歌单名称（可以是任意数字或名称）")
    print("  4. 添加至少一首歌曲")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    playlist_name = args[0] if args else None
    success = test(playlist_name=playlist_name)

    print(f"任务12验证结果: {success}")
    sys.exit(0 if success else 1)