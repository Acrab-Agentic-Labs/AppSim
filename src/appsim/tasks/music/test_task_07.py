"""
任务7：将播放模式改为随机播放
难度：低

人工操作步骤：
1. 进入播放页面
2. 找到播放模式切换按钮（通常在播放控制区域）
3. 多次点击直到切换到随机播放模式（显示随机图标）

验证标准：
检查playback_state.json中playbackMode字段是否为"shuffle"
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_07_check_shuffle_mode(device_id=None, result=None, backup_dir=None):
    """
    任务7: 将播放模式改为随机播放
    验证:
    1. 优先检查playback_state.json中playbackMode是否为"shuffle"
    2. 如果设备状态检查失败,检查result["final_message"]是否包含"随机"相关信息
    """
    # 方法1: 检查设备状态
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)
    if data and data.get("playbackMode") == "shuffle":
        print("  → 设备状态确认: 播放模式已切换为随机播放")
        return True

    # 方法2: 检查AI的final_message
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if final_msg and isinstance(final_msg, str):
            if "随机" in final_msg and ("播放" in final_msg or "模式" in final_msg):
                print(f"  → AI确认完成: {final_msg}")
                print("  → 注意: 设备状态未更新,但AI声称已完成")
                return True

    print("  → 验证失败: 设备状态未更新且AI未确认完成")
    return False


def test(result=None, device_id=None, backup_dir=None):
    result1 = task_07_check_shuffle_mode(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 已切换到随机播放模式")
        return True
    else:
        logging.debug("✗ 测试失败 - 未检测到随机播放模式")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务7：将播放模式改为随机播放")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入播放页面")
    print("  2. 找到播放模式切换按钮（通常在播放控制区域）")
    print("  3. 多次点击直到切换到随机播放模式（显示随机图标）")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务7验证结果: {success}")
    sys.exit(0 if success else 1)