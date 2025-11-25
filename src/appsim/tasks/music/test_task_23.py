"""
任务23：取消收藏第一首歌曲
难度：中

人工操作步骤：
  1. 打开音乐APP
  2. 进入"我的收藏"或播放一首已收藏的歌曲
  3. 点击收藏按钮取消收藏

验证标准：
调用task_23_check_share_to_wechat函数进行验证
检查user_favorites.json中收藏列表是否有变化
"""

import logging
import sys
from .verification_functions import task_23_check_uncollect_song


def test23(result=None, device_id=None, backup_dir=None):
    result1 = task_23_check_uncollect_song(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务23完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务23未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务23：取消收藏第一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入'我的收藏'或播放一首已收藏的歌曲")
    print("  3. 点击收藏按钮取消收藏")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test23(*args)

    print(f"任务23验证结果: {success}")
    sys.exit(0 if success else 1)
