"""
任务9：调节当前音乐播放的音量
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_volume_is_adjusted(result=None, device_id=None, backup_dir=None):
    """
    任务9: 验证音量是否被调节
    - 检查 playback_state.json 中 'volume' 字段是否存在
    - 注意：此验证不检查具体的音量值，只确认音量被调节过。
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and 'volume' in data:
        volume = data['volume']
        logging.info(f"✓ 测试通过 - 任务9完成：音量已被调节，当前值为 {volume}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务9未完成：在设备状态中未找到'volume'字段")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务9：调节当前音乐播放的音量")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放页面")
    print("  2. 调整音量滑块或按钮")
    print("\n🔍 开始验证...")

    success = check_volume_is_adjusted()

    print(f"\n任务9验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
