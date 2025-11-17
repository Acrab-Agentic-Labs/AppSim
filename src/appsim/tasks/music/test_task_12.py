"""
任务12：创建一个新的歌单,并添加首音乐
难度：中

人工操作步骤：
  1. 进入我的页面
  2. 点击创建歌单
  3. 输入歌单名称（可以是任意数字或名称，如"1"、"2"、"测试歌单"等）
  4. 添加歌曲

验证标准：
调用task_12_check_create_playlist_and_add_song函数进行验证

使用方式：
  方式1（推荐）：不传参数，自动检查最新创建的歌单
    python test_task_12.py

  方式2：传入歌单名称，检查指定歌单
    python test_task_12.py 1
    python test_task_12.py 2
    python test_task_12.py 测试歌单
"""

import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .verification_functions import task_12_check_create_playlist_and_add_song


def test12(playlist_name=None, result=None, device_id=None):
    result1 = task_12_check_create_playlist_and_add_song(
        playlist_name=playlist_name, device_id=device_id, result=result
    )

    if result1:
        logging.debug("✓ 测试通过 - 任务12完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务12未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务12：创建一个新的歌单,并添加首音乐")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入我的页面")
    print("  2. 点击创建歌单")
    print("  3. 输入歌单名称（可以是任意数字或名称）")
    print("  4. 添加至少一首歌曲")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    playlist_name = args[0] if args else None
    success = test12(playlist_name=playlist_name)

    print(f"任务12验证结果: {success}")
    sys.exit(0 if success else 1)
