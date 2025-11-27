"""
任务13：搜索"稻香"并播放第一首搜索结果
难度：中

人工操作步骤：
  1. 打开音乐APP
  2. 点击搜索按钮
  3. 输入"稻香"
  4. 点击第一首搜索结果并播放

验证标准：
调用task_13_check_search_and_play函数进行验证
检查search_history.json中是否有搜索"稻香"并播放的记录
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_13_check_search_and_play(search_query="稻香", device_id=None, result=None, backup_dir=None):
    """
    任务13: 搜索"稻香"并播放第一首搜索结果
    验证: 检查search_history.json中有该搜索记录,且action为"play"
    :param search_query: 搜索关键词，默认'稻香'
    """
    data = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir=backup_dir)
    if data and "searches" in data:
        print(f"  → 检查搜索记录: 《{search_query}》")
        for search in data["searches"]:
            if search.get("query") == search_query and search.get("action") == "play":
                print("  → 找到匹配的搜索并播放记录")
                return True
        print(f"  → 未找到搜索《{search_query}》并播放的记录")
    return False


def test(search_query="稻香", result=None, device_id=None, backup_dir=None):
    result1 = task_13_check_search_and_play(search_query=search_query, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务13完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务13未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务13：搜索'稻香'并播放第一首搜索结果")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击搜索按钮")
    print("  3. 输入'稻香'")
    print("  4. 点击第一首搜索结果并播放")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    search_query = args[0] if args else "稻香"
    success = test(search_query=search_query)

    print(f"任务13验证结果: {success}")
    sys.exit(0 if success else 1)