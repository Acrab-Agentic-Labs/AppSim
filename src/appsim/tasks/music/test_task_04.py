"""
任务4：播放每日推荐的歌曲
难度：低

人工操作步骤：
  1. 打开音乐APP
  2. 进入"每日推荐"页面
  3. 点击播放按钮

验证标准：
调用task_04_check_play_song函数进行验证
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_04_check_play_song(device_id=None, result=None, backup_dir=None):
    """
    任务4: 播放当前暂停的歌曲
    验证: 检查playback_state.json中isPlaying是否为true
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)
    if data:
        return data.get("isPlaying") == True
    return False


def test(result=None, device_id=None, backup_dir=None):
    result1 = task_04_check_play_song(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务4完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务4未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务4：播放每日推荐的歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入'每日推荐'页面")
    print("  3. 点击播放按钮")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务4验证结果: {success}")
    sys.exit(0 if success else 1)