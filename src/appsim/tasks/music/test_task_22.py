"""
任务22：查看每周、每月听歌时长
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_listening_stats_is_viewed(result=None, device_id=None, backup_dir=None):
    """
    任务22: 验证是否查看了听歌时长统计
    - 检查 listening_stats.json 中 viewedStats.weekly 或 viewedStats.monthly 是否为 true
    """
    data = read_json_from_device("autotest/listening_stats.json", device_id, result, backup_dir)

    if data and "viewedStats" in data:
        stats = data["viewedStats"]
        if stats.get("weekly") or stats.get("monthly"):
            viewed_type = "周" if stats.get("weekly") else "月"
            logging.info(f"✓ 测试通过 - 任务22完成：已查看听歌{viewed_type}时长统计")
            return True

    logging.error("✗ 测试失败 - 任务22未完成：未检测到周或月听歌时长统计被查看")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务22：查看每周、每月听歌时长")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入'我的'页面")
    print("  2. 点击'听歌时长'或类似入口")
    print("  3. 在统计页面，切换查看周或月统计数据")
    print("\n🔍 开始验证...")

    success = check_listening_stats_is_viewed()

    print(f"\n任务22验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
