"""
任务9：调节当前音乐播放的音量
难度：低
"""

import logging
import sys
from verification_functions import read_json_from_device

def check_volume_is_adjusted(result=None, device_id=None, backup_dir=None):
    """
    任务9: 验证音量是否被调节
    - 首先检查任务是否成功完成（无错误）
    - 然后检查 playback_state.json 中 'volume' 字段是否存在
    """
    # 首先检查任务是否成功完成
    if result and result.get("error"):
        logging.error(f"✗ 测试失败 - 任务9未完成：{result['error']}")
        return False

    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and 'volume' in data:
        volume = data['volume']
        logging.info(f"✓ 测试通过 - 任务9完成：音量已被调节，当前值为 {volume}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务9未完成：在设备状态中未找到'volume'字段")
        return False

if __name__ == "__main__":

    print(check_volume_is_adjusted())
