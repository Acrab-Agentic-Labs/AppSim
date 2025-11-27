"""
任务30：搜索一位歌手，进入歌手主页播放一个MV
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_mv_is_playing(result=None, device_id=None, backup_dir=None):
    """
    任务30: 验证MV是否正在播放
    - 检查 mv_playback.json 中 currentMV.isPlaying 是否为 true
    """
    data = read_json_from_device("autotest/mv_playback.json", device_id, result, backup_dir=backup_dir)

    if data and "currentMV" in data and data["currentMV"].get("isPlaying") == True:
        mv_id = data["currentMV"].get("mvId", "未知MV")
        logging.info(f"✓ 测试通过 - 任务30完成：MV {mv_id} 正在播放")
        return True
    else:
        status = data.get("currentMV", {}) if data else "N/A"
        logging.error(f"✗ 测试失败 - 任务30未完成：未检测到MV正在播放。当前状态: {status}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务30：搜索一位歌手，进入歌手主页播放一个MV")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 搜索一位歌手并进入其主页")
    print("  2. 切换到'MV'标签页")
    print("  3. 点击任意一个MV进行播放")
    print("\n🔍 开始验证...")

    success = check_mv_is_playing()

    print(f"\n任务30验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
