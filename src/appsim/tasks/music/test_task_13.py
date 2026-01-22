"""
任务13：搜索"稻香"并播放第一首搜索结果
难度：中
"""

import logging
import sys
from verification_functions import read_json_from_device

SEARCH_QUERY = "稻香"

def check_search_and_play_song(result=None, device_id=None, backup_dir=None):
    """
    任务13: 验证是否搜索并播放了指定歌曲
    - 检查 search_history.json 中是否有对'稻香'的搜索记录
    - 确保该记录的 action 为 'play'
    """
    data = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir=backup_dir)

    if data and "searches" in data:
        for search in data["searches"]:
            if search.get("query") == SEARCH_QUERY and search.get("action") == "play":
                logging.info(f"✓ 测试通过 - 任务13完成：在搜索历史中找到播放'{SEARCH_QUERY}'的记录")
                return True

    logging.error(f"✗ 测试失败 - 任务13未完成：未在搜索历史中找到播放'{SEARCH_QUERY}'的记录")
    return False

if __name__ == "__main__":

    print(check_search_and_play_song())
