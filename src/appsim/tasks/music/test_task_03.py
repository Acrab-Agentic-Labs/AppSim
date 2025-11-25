"""
任务3：删除‘我的’页面中热歌榜歌单的第一首歌曲
难度：中

人工操作步骤：
  1. 打开音乐APP
  2. 点击底部导航栏的"我的"
  3. 找到"热歌榜"歌单并点击进入
  4. 选中第一首歌曲
  5. 点击删除按钮并确认

验证标准：
调用task_03_delete_first_song_from_hot_playlist函数进行验证
"""

import logging
import sys
from .verification_functions import task_03_delete_first_song_from_hot_playlist


def test3(result=None, device_id=None, backup_dir=None):
    result1 = task_03_delete_first_song_from_hot_playlist(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务3完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务3未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务3：删除‘我的’页面中热歌榜歌单的第一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击底部导航栏的'我的'")
    print("  3. 找到'热歌榜'歌单并点击进入")
    print("  4. 选中第一首歌曲")
    print("  5. 点击删除按钮并确认")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test3(*args)

    print(f"任务3验证结果: {success}")
    sys.exit(0 if success else 1)
