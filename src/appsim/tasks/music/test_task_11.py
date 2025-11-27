"""
任务11：播放"每日推荐"中的第一首歌曲
难度：中

人工操作步骤：
  1. 打开音乐APP
  2. 进入"每日推荐"页面
  3. 点击第一首歌曲播放

验证标准：
调用task_11_check_daily_recommend_third_song函数进行验证
检查playback_state.json中是否显示正在播放每日推荐的第1首歌曲
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_11_check_daily_recommend_third_song(device_id=None, result=None, backup_dir=None):
    """
    任务11: 播放"每日推荐"中的第一首歌曲
    验证: 检查playback_state.json中currentSong.source是否为"daily_recommend"且sourceDetail包含"第1首"
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)
    if data and "currentSong" in data:
        song = data["currentSong"]
        return song.get("source") == "daily_recommend" and "第1首" in song.get("sourceDetail", "")
    return False


def test(result=None, device_id=None, backup_dir=None):
    result1 = task_11_check_daily_recommend_third_song(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务11完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务11未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务11：播放'每日推荐'中的第一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入'每日推荐'页面")
    print("  3. 点击第一首歌曲播放")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务11验证结果: {success}")
    sys.exit(0 if success else 1)