"""
任务10：搜索'丑八怪'并播放，收藏该歌曲，查看歌词，然后切换到下一首歌曲，并设置为随机播放模式
难度：高
类型：复合操作类
"""

import logging
from .verification_functions import read_json_from_device


def check_composite_search_play_favorite_lyrics_next_shuffle(result=None, device_id=None, backup_dir=None):
    """
    任务10: 验证复合操作
    1. 搜索历史包含"丑八怪"
    2. 歌曲被收藏
    3. 歌词已显示
    4. 切换了下一首歌曲（播放记录>=2）
    5. 随机播放模式已启用
    """
    # 1. 检查搜索历史
    search_history = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir)
    if not search_history:
        logging.error("✗ 测试失败 - 任务10未完成：未找到搜索历史")
        return False

    searched = False
    for search in search_history.get("searches", []):
        if "丑八怪" in search.get("query", ""):
            searched = True
            break
    if not searched:
        logging.error("✗ 测试失败 - 任务10未完成：未搜索'丑八怪'")
        return False

    # 2. 检查歌曲是否被收藏
    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        logging.error("✗ 测试失败 - 任务10未完成：未找到收藏数据")
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("丑八怪" in song.get("songName", "") or "丑八怪" in song.get("name", "") for song in favorited_songs):
        logging.error("✗ 测试失败 - 任务10未完成：未收藏'丑八怪'")
        return False

    # 3. 检查歌词是否已显示
    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state:
        logging.error("✗ 测试失败 - 任务10未完成：未找到应用状态")
        return False

    if not app_state.get("lyrics_shown", False) and not app_state.get("showLyrics", False):
        logging.error("✗ 测试失败 - 任务10未完成：未查看歌词")
        return False

    # 4. 检查是否切换了歌曲
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    records = []
    if play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
    if len(records) < 2:
        logging.error("✗ 测试失败 - 任务10未完成：未切换到下一首歌曲")
        return False

    # 5. 检查随机播放模式
    player_settings = read_json_from_device("autotest/player_settings.json", device_id, result, backup_dir)
    if not player_settings:
        logging.error("✗ 测试失败 - 任务10未完成：未找到播放器设置")
        return False

    if not player_settings.get("shuffle_mode", False) and not player_settings.get("shuffleMode", False):
        logging.error("✗ 测试失败 - 任务10未完成：未设置随机播放模式")
        return False

    logging.info("✓ 测试通过 - 任务10完成：搜索丑八怪、播放、收藏、查看歌词、切换下一首、设置随机播放")
    return True


if __name__ == "__main__":
    print(check_composite_search_play_favorite_lyrics_next_shuffle())
