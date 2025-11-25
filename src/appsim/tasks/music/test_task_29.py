"""
任务29：将关注列表中的一位歌手删除
难度：高

人工操作步骤：
  1. 进入关注列表
  2. 找到歌手
  3. 取消关注

验证标准：
调用task_29_check_unfollow_artist函数进行验证

参数：artist_id，默认'artist_002'
"""

import logging

import sys

from .verification_functions import task_29_check_unfollow_artist


def test29(artist_id=None, result=None, device_id=None, backup_dir=None):
    result1 = task_29_check_unfollow_artist(artist_id=artist_id, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务29完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务29未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务29：将关注列表中的一位歌手删除")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入关注列表")
    print("  2. 找到歌手")
    print("  3. 取消关注")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    artist_id = args[0] if args else None
    success = test29(artist_id=artist_id)

    print(f"任务29验证结果: {success}")
    sys.exit(0 if success else 1)
