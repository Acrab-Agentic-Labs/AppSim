"""
任务31：更改播放器样式
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_player_style_is_changed(result=None, device_id=None, backup_dir=None):
    """
    任务31: 验证播放器样式是否已更改
    - 检查 player_settings.json 中 playerStyle.styleId 是否不是默认值（例如 'default_style'）
    """
    data = read_json_from_device("autotest/player_settings.json", device_id, result, backup_dir)

    if data and "playerStyle" in data:
        style_id = data["playerStyle"].get("styleId", "default_style")
        if style_id != "default_style":
            logging.info(f"✓ 测试通过 - 任务31完成：播放器样式已更改为 '{style_id}'")
            return True
        else:
            logging.error("✗ 测试失败 - 任务31未完成：播放器样式仍为默认值")
            return False

    logging.error("✗ 测试失败 - 任务31未完成：在设备状态中未找到播放器样式信息")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务31：更改播放器样式")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入歌曲播放页面")
    print("  2. 打开更多选项或设置")
    print("  3. 进入'播放器样式'或'主题'设置")
    print("  4. 选择一个新的样式")
    print("\n🔍 开始验证...")

    success = check_player_style_is_changed()

    print(f"\n任务31验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
