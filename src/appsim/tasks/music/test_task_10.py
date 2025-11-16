"""
任务10：随机进入'我的'中的一个歌单
难度：低

人工操作步骤：
  1. 进入我的页面
  2. 点击任意一个歌单

验证标准：
调用task_10_check_enter_playlist函数进行验证
"""

import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .verification_functions import task_10_check_enter_playlist


def test10(result=None, device_id=None):
    result1 = task_10_check_enter_playlist(device_id=device_id, result=result)

    if result1:
        logging.debug("✓ 测试通过 - 任务10完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务10未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务10：随机进入'我的'中的一个歌单")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入我的页面")
    print("  2. 点击任意一个歌单")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test10(*args)

    print(f"任务10验证结果: {success}")
    sys.exit(0 if success else 1)
