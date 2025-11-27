"""
任务16：查看一首歌曲的歌词
难度：中

人工操作步骤：
  1. 进入播放页面
  2. 点击显示歌词按钮

验证标准：
调用task_16_check_view_lyrics函数进行验证
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_16_check_view_lyrics(device_id=None, result=None, backup_dir=None):
    """
    任务16: 查看一首歌曲的歌词
    验证: 检查app_state.json中showLyrics为true或currentPage为"lyrics"
    """
    data = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir=backup_dir)
    if data:
        return data.get("showLyrics") == True or data.get("currentPage") == "lyrics"
    return False

def test(result=None, device_id=None, backup_dir=None):
    result1 = task_16_check_view_lyrics(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务16完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务16未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务16：查看一首歌曲的歌词")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放页面")
    print("  2. 点击显示歌词按钮")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务16验证结果: {success}")
    sys.exit(0 if success else 1)