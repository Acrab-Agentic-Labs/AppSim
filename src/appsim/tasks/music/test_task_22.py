"""
任务22：查看每周、每月听歌时长
难度：高

人工操作步骤：
  1. 进入我的页面
  2. 点击听歌时长
  3. 查看周/月统计

验证标准：
调用task_22_check_view_listening_stats函数进行验证

参数：stat_type（'weekly'或'monthly'），默认自动检测
"""

import logging
import sys
from .verification_functions import read_json_from_device, task_22_check_view_listening_stats


def test22(stat_type=None, result=None, device_id=None, backup_dir=None):
    # 如果没有指定stat_type，自动从listening_stats.json检测查看过的统计类型
    if stat_type is None:
        stats_data = read_json_from_device("autotest/listening_stats.json", device_id=device_id, result=result, backup_dir=backup_dir)

        if stats_data and "viewedStats" in stats_data:
            viewed_stats = stats_data["viewedStats"]
            weekly_viewed = viewed_stats.get("weekly", False)
            monthly_viewed = viewed_stats.get("monthly", False)

            # 优先检测最近查看的（假设两者都为True时，选择monthly）
            if monthly_viewed:
                stat_type = "monthly"
            elif weekly_viewed:
                stat_type = "weekly"
            else:
                logging.debug("✗ 错误：未检测到查看过的统计")
                return False
        else:
            logging.debug("✗ 错误：无法读取统计数据")
            return False

    result1 = task_22_check_view_listening_stats(stat_type, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        stat_name = "月度统计" if stat_type == "monthly" else "周统计"
        logging.debug(f"✓ 测试通过 - 已查看{stat_name}")
        return True
    else:
        stat_name = "月度统计" if stat_type == "monthly" else "周统计"
        logging.debug(f"✗ 测试失败 - 未查看{stat_name}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务22：查看每周、每月听歌时长")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入我的页面")
    print("  2. 点击听歌时长")
    print("  3. 查看周/月统计")

    # 可以通过命令行参数传入stat_type
    # 用法1：python test_task_22.py          # 自动检测
    # 用法2：python test_task_22.py weekly   # 手动指定周统计
    # 用法3：python test_task_22.py monthly  # 手动指定月度统计
    stat_type = sys.argv[1] if len(sys.argv) > 1 else None
    success = test22(stat_type=stat_type)

    print(f"任务22验证结果: {success}")
    sys.exit(0 if success else 1)
