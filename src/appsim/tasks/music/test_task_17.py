"""
任务17：漫游播放并设置播放场景为"伪感"
难度：中

人工操作步骤：
1. 进入漫游页面（点击底部"漫游"按钮）
2. 点击场景选择按钮（通常在页面上方）
3. 在场景列表中找到并点击"伪感"场景
4. 确认场景已切换

验证标准：
检查player_settings.json中strollMode.scene字段是否为"伪感"

注意：可以测试其他场景，通过命令行参数传入场景名称
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_17_check_stroll_scene_setting(scene_name, device_id=None, result=None, backup_dir=None):
    """
    任务17: 漫游播放并设置播放场景为"伪感"
    验证: 检查player_settings.json中strollMode.scene是否为指定场景
    :param scene_name: 场景名称,如"伪感"
    """
    data = read_json_from_device("autotest/player_settings.json", device_id, result, backup_dir=backup_dir)
    if data and "strollMode" in data:
        return data["strollMode"].get("scene") == scene_name
    return False


def test(scene_name="欢快", result=None, device_id=None, backup_dir=None):
    result1 = task_17_check_stroll_scene_setting(scene_name, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug(f"✓ 测试通过 - 场景已设置为'{scene_name}'")
        return True
    else:
        logging.debug(f"✗ 测试失败 - 场景未设置为'{scene_name}'")
        return False


if __name__ == "__main__":
    print("=" * 70)
    scene_name = sys.argv[1] if len(sys.argv) > 1 else "欢快"
    print(f"任务17：漫游播放并设置播放场景为'{scene_name}'")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入漫游页面（点击底部'漫游'按钮）")
    print("  2. 点击场景选择按钮（通常在页面上方）")
    print(f"  3. 在场景列表中找到并点击'{scene_name}'场景")
    print("  4. 确认场景已切换")
    print(f"\n🔍 开始验证... (检查场景: {scene_name})")

    # 可以通过命令行参数传入场景名称
    # 用法：python test_task_17.py 伤感
    # 或：python test_task_17.py 欢快
    success = test(scene_name=scene_name)

    print(f"任务17验证结果: {success}")
    sys.exit(0 if success else 1)