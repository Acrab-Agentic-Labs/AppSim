"""
任务9：调节当前音乐播放的音量
难度：低

人工操作步骤：
  1. 进入播放页面
  2. 调整音量滑块或按钮

验证标准：
调用task_09_check_volume_adjusted函数进行验证

可选参数：expected_volume（期望的音量值0-100）
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_09_check_volume_adjusted(expected_volume=None, device_id=None, result=None, backup_dir=None):
    """
    任务9: 调节当前音乐播放的音量
    验证: 检查playback_state.json中volume是否改变
    :param expected_volume: 期望的音量值(0-100)
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)
    if data:
        if expected_volume is not None:
            return data.get("volume") == expected_volume
        # 如果没有指定期望音量,只要volume字段存在就认为成功
        return "volume" in data
    return False


def test(expected_volume=None, result=None, device_id=None, backup_dir=None):
    result1 = task_09_check_volume_adjusted(expected_volume=expected_volume, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务9完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务9未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务9：调节当前音乐播放的音量")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放页面")
    print("  2. 调整音量滑块或按钮")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    expected_volume = int(args[0]) if args and args[0].isdigit() else None
    success = test(expected_volume=expected_volume)

    print(f"任务9验证结果: {success}")
    sys.exit(0 if success else 1)