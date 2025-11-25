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
from .verification_functions import task_07_check_shuffle_play


def test7(result=None, device_id=None, backup_dir=None):
    result1 = task_07_check_shuffle_play(device_id=device_id, result=result, backup_dir=backup_dir)

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
    success = test7(*args)

    print(f"任务7验证结果: {success}")
    sys.exit(0 if success else 1)
