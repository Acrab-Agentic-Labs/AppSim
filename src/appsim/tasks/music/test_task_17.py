"""
任务17：漫游播放并设置播放场景为"伪感"
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

SCENE_NAME = "伪感"

def check_stroll_scene_is_set(result=None, device_id=None, backup_dir=None):
    """
    任务17: 验证漫游播放场景是否已设置为'伪感'
    - 检查 player_settings.json 中 strollMode.scene 是否为 '伪感'
    """
    data = read_json_from_device("autotest/player_settings.json", device_id, result, backup_dir=backup_dir)

    if data and "strollMode" in data and data["strollMode"].get("scene") == SCENE_NAME:
        logging.info(f"✓ 测试通过 - 任务17完成：漫游场景已设置为'{SCENE_NAME}'")
        return True
    else:
        scene = data.get('strollMode', {}).get('scene') if data else 'N/A'
        logging.error(f"✗ 测试失败 - 任务17未完成：漫游场景设置不正确。期望: '{SCENE_NAME}', 实际: '{scene}'")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print(f"任务17：漫游播放并设置播放场景为'{SCENE_NAME}'")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入'漫游'页面")
    print("  2. 点击场景选择按钮")
    print(f"  3. 在场景列表中找到并点击'{SCENE_NAME}'")
    print("\n🔍 开始验证...")

    success = check_stroll_scene_is_set()

    print(f"\n任务17验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
