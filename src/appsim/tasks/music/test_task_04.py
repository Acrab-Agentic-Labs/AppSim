"""
任务4：播放每日推荐的歌曲
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_is_playing(result=None, device_id=None, backup_dir=None):
    """
    任务4: 验证歌曲是否正在播放
    - 检查 playback_state.json 中 isPlaying 是否为 true
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and data.get("isPlaying") == True:
        logging.info("✓ 测试通过 - 任务4完成：歌曲正在播放")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务4未完成：歌曲未在播放。检查到的状态是: {data.get('isPlaying') if data else 'N/A'}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务4：播放每日推荐的歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入'每日推荐'页面")
    print("  3. 点击播放按钮")
    print("\n🔍 开始验证...")

    success = check_is_playing()

    print(f"\n任务4验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
