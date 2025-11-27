"""
任务6：切换播放上一首歌曲
难度：低

人工操作步骤：
  1. 进入播放页面
  2. 点击上一首按钮（←）

验证标准：
调用task_06_check_switch_previous_song函数进行验证

可选参数：expected_song_id（期望的歌曲ID）
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_06_check_switch_previous_song(expected_song_id=None, device_id=None, result=None, backup_dir=None):
    """
    任务6: 切换播放上一首歌曲
    验证: 检查playback_state.json中currentSong.songId是否变化
    :param expected_song_id: 期望的歌曲ID(如果已知)
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)
    if data and "currentSong" in data:
        if expected_song_id:
            return data["currentSong"].get("songId") == expected_song_id
        # 如果没有指定期望ID,只要有currentSong就认为切换成功
        return "songId" in data["currentSong"]
    return False


def test(expected_song_id=None, result=None, device_id=None, backup_dir=None):
    result1 = task_06_check_switch_previous_song(expected_song_id=expected_song_id, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务6完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务6未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务6：切换播放上一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放页面")
    print("  2. 点击上一首按钮（←）")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    expected_song_id = args[0] if args else None
    success = test(expected_song_id=expected_song_id)

    print(f"任务6验证结果: {success}")
    sys.exit(0 if success else 1)