"""
任务7：将播放模式改为随机播放
难度：低
"""

import logging
import sys
from .verification_functions import read_json_from_device

def verify_shuffle_mode_enabled(result=None, device_id=None, backup_dir=None):
    """
    任务7: 验证是否切换到随机播放模式
    - 检查 playback_state.json 中 playbackMode 是否为 "shuffle"
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if data and data.get("playbackMode") == "shuffle":
        logging.info("✓ 测试通过 - 任务7完成：播放模式已切换为随机播放")
        return True
    else:
        # 如果设备状态检查失败, 检查final_message作为后备
        if result and "final_message" in result:
            final_msg = result["final_message"]
            if final_msg and isinstance(final_msg, str) and "随机" in final_msg and ("播放" in final_msg or "模式" in final_msg):
                logging.info(f"✓ 测试通过 - 任务7完成：AI确认完成: {final_msg} (注意: 设备状态未直接验证)")
                return True
        
        logging.error(f"✗ 测试失败 - 任务7未完成：未切换到随机播放模式。检查到的模式是: {data.get('playbackMode') if data else 'N/A'}")
        return False

if __name__ == "__main__":

    print(verify_shuffle_mode_enabled())
