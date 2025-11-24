"""
任务3：进入"我的"页面
难度：低

人工操作步骤：
  1. 打开音乐APP
  2. 点击底部导航栏的"我的"

验证标准：
调用task_03_check_navigate_to_profile函数进行验证
"""

import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .verification_functions import task_03_check_navigate_to_profile


def test3(result=None, device_id=None):
    result1 = task_03_check_navigate_to_profile(device_id=device_id, result=result)

    if result1:
        logging.debug("✓ 测试通过 - 任务3完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务3未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务3：进入我的页面")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击底部导航栏的'我的'")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test3(*args)

    print(f"任务3验证结果: {success}")
    sys.exit(0 if success else 1)
