"""
任务32：数一下歌曲《晴天》的评论数目
难度：中
类型：信息检索/推理类
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device

# 假设《晴天》在测试环境中的歌曲ID是 'song_001'
SONG_ID_FOR_TASK = "song_001"

def check_comment_count(result=None, device_id=None, backup_dir=None):
    """
    任务32: 核实《晴天》的评论数
    - 从AI回答中解析出评论数
    - 从设备读取comments.json计算实际评论数
    - 对比两者是否一致
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务32未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务32未完成：final_message格式错误: {final_msg}")
        return False

    # 1. 从AI回答中解析出数字
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"✗ 测试失败 - 任务32未完成：未能在AI的回答中找到任何数字: '{final_msg}'")
        return False
    agent_count = int(numbers[0])
    logging.info(f"  → AI报告的评论数为: {agent_count}")

    # 2. 从设备读取真实数据
    comments_data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments_data or "allComments" not in comments_data or not isinstance(comments_data.get("allComments"), dict):
        logging.error("✗ 测试失败 - 任务32未完成：无法从设备读取评论数据或'allComments'字段格式不正确")
        return False

    # 3. 计算真实值
    device_count = 0
    if SONG_ID_FOR_TASK in comments_data["allComments"]:
        device_count = len(comments_data["allComments"][SONG_ID_FOR_TASK])
    logging.info(f"  → 设备中歌曲'{SONG_ID_FOR_TASK}'的实际评论数为: {device_count}")

    # 4. 对比验证
    if agent_count == device_count:
        logging.info("✓ 测试通过 - 任务32完成：AI报告的评论数与设备实际评论数一致")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务32未完成：AI报告的评论数({agent_count})与设备实际评论数({device_count})不符")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务32：数一下歌曲《晴天》的评论数目")
    print("=" * 70)
    print("\n🔍 开始验证...")

    mock_result = { "final_message": "这首歌有 50 条评论。" }
    success = check_comment_count(result=mock_result)

    print(f"\n任务32验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)