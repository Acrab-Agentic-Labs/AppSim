"""
任务2：在‘我的’页面的所有歌单中哪一个歌单里的歌曲数量最多
难度：中
类型：推理类

人工操作步骤：
  1. 打开音乐APP
  2. 点击底部导航栏的"我的"
  3. 查看所有歌单及其歌曲数量
  4. 找出数量最多的歌单并返回其名称

验证标准：
调用task_02_find_playlist_with_most_songs函数进行验证
"""

import logging
import sys
from .verification_functions import task_02_find_playlist_with_most_songs


def test2(result=None, device_id=None, backup_dir=None):
    result1 = task_02_find_playlist_with_most_songs(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务2完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务2未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务2：在‘我的’页面的所有歌单中哪一个歌单里的歌曲数量最多")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击底部导航栏的'我的'")
    print("  3. 查看所有歌单及其歌曲数量")
    print("  4. 找出数量最多的歌单并返回其名称")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test2(*args)

    print(f"任务2验证结果: {success}")
    sys.exit(0 if success else 1)
