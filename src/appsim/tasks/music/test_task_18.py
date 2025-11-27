"""
任务18：进入排行榜的新歌榜，告诉我榜单名称
难度：中
类型：信息检索类
"""

import logging
import sys

def check_rank_name_is_reported(result=None, device_id=None, backup_dir=None):
    """
    任务18: 验证AI是否返回了榜单名称
    - 检查 final_message 中是否包含'榜'、'新歌'等关键词
    - 注意：这是一个信息检索任务，不直接验证设备状态。
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务18未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if final_msg and isinstance(final_msg, str):
        if "榜" in final_msg or "新歌" in final_msg or "排行" in final_msg:
            logging.info(f"✓ 测试通过 - 任务18完成：AI返回了榜单信息: '{final_msg}'")
            return True
        else:
            logging.error(f"✗ 测试失败 - 任务18未完成：AI返回的消息中未包含榜单关键词: '{final_msg}'")
            return False
            
    logging.error(f"✗ 测试失败 - 任务18未完成：final_message格式错误: {final_msg}")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务18：进入排行榜的新歌榜，告诉我榜单名称")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP，进入'排行榜'页面")
    print("  2. 找到并点击'新歌榜'")
    print("  3. AI应返回榜单名称")
    print("\n🔍 开始验证...")

    mock_result = {
        "final_message": "这个榜单是新歌榜。"
    }
    success = check_rank_name_is_reported(result=mock_result)

    print(f"\n任务18验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
