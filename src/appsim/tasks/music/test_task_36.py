"""
任务36：数一下我的粉丝数目
难度：低
类型：信息检索类

人工操作步骤：
  1. 打开音乐APP
  2. 进入"我的"页面
  3. 找到并进入个人主页或“我的粉丝”页面
  4. 查看并返回粉丝数量

验证标准：
调用task_36_check_follower_count函数进行验证
AI返回的粉丝数必须与设备文件fan_items.json中实际粉丝数相符
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device


def task_36_check_follower_count(result=None, device_id=None, backup_dir=None):
    """
    任务36: 核实我的粉丝数目
    验证: 1. 从AI回答解析出数目. 2. 从设备读取fan_items.json获取真实数目. 3. 对比.
    """
    if not result or "final_message" not in result:
        logging.error("  → AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"  → final_message格式错误: {final_msg}")
        return False

    # 1. 从AI回答中解析出数字
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"  → 未能在AI的回答中找到任何数字: {final_msg}")
        return False
    agent_count = int(numbers[0])
    logging.info(f"  → AI报告的粉丝数为: {agent_count}")

    # 2. 从设备读取真实数据
    fan_items_data = read_json_from_device("autotest/fan_items.json", device_id, result, backup_dir)
    # 假设文件结构为一个粉丝对象列表: [...] 
    if not isinstance(fan_items_data, list):
        logging.error("  → 无法从设备读取粉丝数据或数据格式不正确 (应为列表)")
        return False

    # 3. 获取真实值
    device_count = len(fan_items_data)
    logging.info(f"  → 设备中的实际粉丝数为: {device_count}")

    # 4. 对比验证
    if agent_count == device_count:
        logging.info("  → 验证成功: AI报告的粉丝数与设备实际情况一致")
        return True
    else:
        logging.error(f"  → 验证失败: AI报告的粉丝数({agent_count})与设备实际情况({device_count})不符")
        return False


def test(result=None, device_id=None, backup_dir=None):
    """
    执行任务36的测试
    """
    if task_36_check_follower_count(result, device_id, backup_dir):
        logging.info("✓ 测试通过 - 任务36完成")
        return True
    else:
        logging.error("✗ 测试失败 - 任务36未完成")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务36：数一下我的粉丝数目")
    print("=" * 70)
    print("\n🔍 开始验证...")

    mock_result = { "final_message": "您目前有 5 位粉丝。" } # 根据 fan_items.json 文件的内容，这里假设有 5 位粉丝
    success = test(result=mock_result)

    print(f"\n任务36验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
