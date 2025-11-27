"""
任务5：暂停播放当前的歌曲
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_is_paused(result=None, device_id=None, backup_dir=None):
    """
    任务5: 验证歌曲是否已暂停
    - 检查 playback_state.json 中 isPlaying 是否为 false
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and data.get("isPlaying") == False:
        logging.info("✓ 测试通过 - 任务5完成：歌曲已暂停")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务5未完成：歌曲未暂停。检查到的状态是: {data.get('isPlaying') if data else 'N/A'}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务5：暂停播放当前的歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放页面")
    print("  2. 点击暂停按钮")
    print("\n🔍 开始验证...")

    success = check_is_paused()

    print(f"\n任务5验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
