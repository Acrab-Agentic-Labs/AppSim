"""
任务16：查看一首歌曲的歌词
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_lyrics_are_shown(result=None, device_id=None, backup_dir=None):
    """
    任务16: 验证是否查看了歌词
    - 检查 app_state.json 中 showLyrics 是否为 true 或 currentPage 是否为 'lyrics'
    """
    data = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir=backup_dir)

    if data and (data.get("showLyrics") == True or data.get("currentPage") == "lyrics"):
        logging.info("✓ 测试通过 - 任务16完成：歌词正在显示")
        return True
    else:
        page = data.get('currentPage') if data else 'N/A'
        show_lyrics = data.get('showLyrics') if data else 'N/A'
        logging.error(f"✗ 测试失败 - 任务16未完成：未检测到歌词显示。当前页面: '{page}', showLyrics状态: {show_lyrics}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务16：查看一首歌曲的歌词")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入歌曲播放页面")
    print("  2. 点击歌曲封面或歌词显示区域以展开歌词")
    print("\n🔍 开始验证...")

    success = check_lyrics_are_shown()

    print(f"\n任务16验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
