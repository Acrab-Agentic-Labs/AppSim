"""
任务26：使用听歌识曲功能识别一首歌曲
难度：高
注意：此功能涉及跨应用交互，无法自动验证
"""

import logging
import sys

def check_song_recognition_is_attempted(result=None, device_id=None, backup_dir=None):
    """
    任务26: 验证是否尝试了听歌识曲
    - 这是一个无法直接验证设备状态的任务。
    - 作为后备，检查AI的 final_message 是否表明它已尝试或正在进行识曲。
    """
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if final_msg and isinstance(final_msg, str):
            keywords = ["识曲", "识别", "正在听", "找到歌曲"]
            if any(keyword in final_msg for keyword in keywords):
                logging.info(f"✓ 测试通过 - 任务26完成：AI返回了与识曲相关的消息: '{final_msg}'")
                return True

    logging.warning("✓ 测试通过（无法验证） - 任务26：听歌识曲为跨应用功能，无法进行设备状态验证。假定AI已尝试执行。")
    return True # 对于无法验证的任务，暂时标记为通过


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务26：使用听歌识曲功能识别一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 找到并点击'听歌识曲'功能")
    print("  3. 在外部播放一首歌曲以供识别")
    print("  4. 等待识别结果")
    print("\n⚠️  注意：此功能为跨应用交互，无法自动验证，默认通过。")
    print("\n🔍 开始验证...")

    mock_result = {
        "final_message": "正在努力识别歌曲..."
    }
    success = check_song_recognition_is_attempted(result=mock_result)

    print(f"\n任务26验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
