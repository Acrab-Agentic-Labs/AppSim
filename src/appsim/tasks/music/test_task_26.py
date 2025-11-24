"""
任务26：使用听歌识曲功能识别一首歌曲
难度：高
注意：此功能涉及跨应用交互，可能难以自动验证

人工操作步骤：
  1. 打开音乐APP
  2. 找到并点击"听歌识曲"功能
  3. 播放一首歌曲（可以从其他APP或外部音源）
  4. 等待识别结果

验证标准：
调用task_26_check_song_recognition函数进行验证
由于跨应用功能难以验证，此验证函数返回False表示不支持自动验证
"""

import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .verification_functions import task_26_check_song_recognition


def test26(result=None, device_id=None):
    result1 = task_26_check_song_recognition(device_id=device_id, result=result)

    if result1:
        logging.debug("✓ 测试通过 - 任务26完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务26未完成或不支持自动验证")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务26：使用听歌识曲功能识别一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 找到并点击'听歌识曲'功能")
    print("  3. 播放一首歌曲（可以从其他APP或外部音源）")
    print("  4. 等待识别结果")
    print("\n⚠️  注意：此功能涉及跨应用交互")
    print("   可能难以自动验证，需要人工确认")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test26(*args)

    print(f"任务26验证结果: {success}")
    sys.exit(0 if success else 1)
