"""
任务25：进入个人听歌时长页面，告诉我本周听歌时长是多少
难度：中
类型：信息检索类

人工操作步骤：
  1. 打开音乐APP
  2. 进入"我的"页面
  3. 找到并点击"听歌时长"或"统计"相关入口
  4. 查看本周听歌时长

验证标准：
调用task_25_check_invite_friend函数进行验证
这是信息检索类任务，AI应该返回时长信息，验证result["final_message"]中是否包含时长相关信息
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_25_check_invite_friend(device_id=None, result=None, backup_dir=None):
    """
    任务25: 进入个人听歌时长页面,告诉我本周听歌时长是多少
    验证: 这是信息检索类任务,检查result["final_message"]中是否包含时长相关信息
    """
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if final_msg and isinstance(final_msg, str):
            # 检查是否包含时长相关信息（小时、分钟、时长等）
            time_keywords = ["小时", "分钟", "时长", "hour", "minute", "min", "h"]
            has_time_keyword = any(keyword in final_msg for keyword in time_keywords)
            # 检查是否包含数字
            import re
            has_number = bool(re.search(r'\d+', final_msg))

            if has_time_keyword and has_number:
                print(f"  → AI返回了时长信息: {final_msg}")
                return True
            else:
                print(f"  → AI返回的消息中未包含有效的时长信息: {final_msg}")
                return False
    print("  → 未找到final_message或格式不正确")
    return False


def test(result=None, device_id=None, backup_dir=None):
    result1 = task_25_check_invite_friend(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务25完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务25未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务25：进入个人听歌时长页面，告诉我本周听歌时长是多少")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入'我的'页面")
    print("  3. 找到并点击'听歌时长'或'统计'相关入口")
    print("  4. 查看本周听歌时长")
    print("\n⚠️  注意：这是信息检索类任务")
    print("   AI应该找到时长信息并告诉你具体数值")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务25验证结果: {success}")
    sys.exit(0 if success else 1)