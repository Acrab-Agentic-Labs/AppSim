"""
任务16：查看一首歌曲的歌词
难度：中
"""

import logging
import sys
from verification_functions import read_json_from_device

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

    print(check_lyrics_are_shown())
