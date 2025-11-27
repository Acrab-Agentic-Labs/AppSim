"""
任务1：进入‘我的’页面中‘我喜欢的音乐’这个歌单
难度：低

人工操作步骤：
  1. 打开音乐APP
  2. 点击底部导航栏的"我的"
  3. 点击"我喜欢的音乐"歌单

验证标准：
调用task_01_check_enter_favorite_playlist函数进行验证
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_01_check_enter_favorite_playlist(device_id=None, result=None, backup_dir=None):
    """
    任务1: 进入'我喜欢的音乐'歌单
    验证: 检查user_playlists.json中currentViewingPlaylist是否为"favorites"
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)
    if data:
        return data.get("currentViewingPlaylist") == "favorites"
    return False


def test(result=None, device_id=None, backup_dir=None):
    result1 = task_01_check_enter_favorite_playlist(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务1完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务1未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务1：进入‘我的’页面中‘我喜欢的音乐’这个歌单")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击底部导航栏的'我的'")
    print("  3. 点击'我喜欢的音乐'歌单")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务1验证结果: {success}")
    sys.exit(0 if success else 1)