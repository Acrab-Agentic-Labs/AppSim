"""
任务31：更改播放器样式
难度：高

人工操作步骤：
  1. 进入播放器设置
  2. 选择样式

验证标准：
调用task_31_check_change_player_style函数进行验证

参数：style_id，默认自动检测
"""

import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .verification_functions import read_json_from_device, task_31_check_change_player_style


def test31(style_id=None, result=None, device_id=None):
    # 如果没有指定style_id，自动从player_settings.json获取当前播放器样式
    if style_id is None:
        settings_data = read_json_from_device("autotest/player_settings.json", device_id=device_id, result=result)

        if settings_data and "playerStyle" in settings_data and settings_data["playerStyle"]:
            style_id = settings_data["playerStyle"].get("styleId")
        else:
            logging.debug("✗ 错误：无法检测到当前播放器样式")
            return False

    result1 = task_31_check_change_player_style(style_id, device_id=device_id, result=result)

    if result1:
        logging.debug(f"✓ 测试通过 - 播放器样式已设置为 {style_id}")
        return True
    else:
        logging.debug(f"✗ 测试失败 - 播放器样式未设置为 {style_id}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务31：更改播放器样式")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放器设置")
    print("  2. 选择样式")

    # 可以通过命令行参数传入style_id
    # 用法1：python test_task_31.py          # 自动检测当前样式
    # 用法2：python test_task_31.py style_002  # 手动指定样式ID
    style_id = sys.argv[1] if len(sys.argv) > 1 else None
    success = test31(style_id=style_id)

    print(f"任务31验证结果: {success}")
    sys.exit(0 if success else 1)
