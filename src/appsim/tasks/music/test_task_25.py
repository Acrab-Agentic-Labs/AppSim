"\n"
import logging
import sys
import re

def check_weekly_listening_duration_is_reported(result=None, device_id=None, backup_dir=None):
    """
    任务25: 验证AI是否返回了本周听歌时长
    - 检查 final_message 中是否包含数字以及'小时'、'分钟'等时间关键词
    - 注意：这是一个信息检索任务，不直接验证设备状态。
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务25未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务25未完成：final_message格式错误: {final_msg}")
        return False

    # 检查是否包含数字和时间关键词
    has_number = bool(re.search(r'\d+', final_msg))
    time_keywords = ["小时", "分钟", "时长", "hour", "minute", "min", "h"]
    has_time_keyword = any(keyword in final_msg for keyword in time_keywords)

    if has_number and has_time_keyword:
        logging.info(f"✓ 测试通过 - 任务25完成：AI返回了时长信息: '{final_msg}'")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务25未完成：AI返回的消息中未包含有效的时长信息: '{final_msg}'")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务25：进入个人听歌时长页面，告诉我本周听歌时长是多少")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP，进入'我的'页面")
    print("  2. 找到并点击'听歌时长'或'统计'入口")
    print("  3. 查看本周听歌时长并告知用户")
    print("\n🔍 开始验证...")

    mock_result = {
        "final_message": "您本周的听歌时长是 5 小时 20 分钟。"
    }
    success = check_weekly_listening_duration_is_reported(result=mock_result)

    print(f"\n任务25验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
