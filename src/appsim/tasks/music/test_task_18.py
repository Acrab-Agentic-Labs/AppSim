"""
任务18：进入排行榜的新歌榜，告诉我榜单名称
难度：中
类型：信息检索类

人工操作步骤：
  1. 打开音乐APP
  2. 进入"排行榜"页面
  3. 找到并点击"新歌榜"

验证标准：
调用task_18_check_copy_comment函数进行验证
这是信息检索类任务，AI应该返回榜单名称，验证result["final_message"]中是否包含榜单相关信息
"""

import logging
import sys
from .verification_functions import task_18_check_billboard_and_tell_name


def test18(result=None, device_id=None, backup_dir=None):
    result1 = task_18_check_copy_comment(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务18完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务18未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务18：进入排行榜的新歌榜，告诉我榜单名称")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入'排行榜'页面")
    print("  3. 找到并点击'新歌榜'")
    print("\n⚠️  注意：这是信息检索类任务")
    print("   AI应该找到榜单并告诉你榜单名称")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test18(*args)

    print(f"任务18验证结果: {success}")
    sys.exit(0 if success else 1)
