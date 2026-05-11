"""
任务25：搜索'薛之谦'，进入歌手主页，播放"演员"，收藏该歌曲，查看歌词并告诉我第一句歌词，并播放MV
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device


def check_composite_xuezhiqian_play_favorite_lyrics_mv(result=None, device_id=None, backup_dir=None):
    """
    任务25: 验证复合操作
    1. 搜索历史包含"薛之谦"
    2. 播放了"演员"
    3. 歌曲被收藏
    4. 歌词已显示
    5. AI回答包含第一句歌词"简单点说话的方式简单点"
    6. MV正在播放
    """
    # 1. 检查搜索历史
    search_history = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir)
    if not search_history:
        logging.error("✗ 测试失败 - 任务25未完成：未找到搜索历史")
        return False

    searched = False
    for search in search_history.get("searches", []):
        if "薛之谦" in search.get("query", ""):
            searched = True
            break
    if not searched:
        logging.error("✗ 测试失败 - 任务25未完成：未搜索'薛之谦'")
        return False

    # 2. 检查是否播放了"演员"
    playback_state = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    if not playback_state:
        logging.error("✗ 测试失败 - 任务25未完成：未找到播放状态")
        return False

    current_song = playback_state.get("currentSong", {})
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    played_yangyuan = False
    if current_song and "演员" in current_song.get("songName", ""):
        played_yangyuan = True
    elif play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
        for record in records:
            if isinstance(record, dict) and ("演员" in record.get("songName", "") or "演员" in record.get("name", "")):
                played_yangyuan = True
                break
    if not played_yangyuan:
        logging.error("✗ 测试失败 - 任务25未完成：未播放'演员'")
        return False

    # 3. 检查歌曲是否被收藏
    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        logging.error("✗ 测试失败 - 任务25未完成：未找到收藏数据")
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("演员" in song.get("songName", "") or "演员" in song.get("name", "") for song in favorited_songs):
        logging.error("✗ 测试失败 - 任务25未完成：未收藏'演员'")
        return False

    # 4. 检查歌词是否已显示
    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state:
        logging.error("✗ 测试失败 - 任务25未完成：未找到应用状态")
        return False

    if not app_state.get("lyrics_shown", False) and not app_state.get("showLyrics", False):
        logging.error("✗ 测试失败 - 任务25未完成：未查看歌词")
        return False

    # 5. 检查AI回答是否包含第一句歌词
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务25未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or "简单点说话的方式简单点" not in final_msg:
        logging.error(f"✗ 测试失败 - 任务25未完成：AI未正确报告第一句歌词。回答: '{final_msg}'")
        return False

    # 6. 检查MV是否在播放
    mv_state = read_json_from_device("autotest/mv_playback.json", device_id, result, backup_dir)
    if not mv_state:
        logging.error("✗ 测试失败 - 任务25未完成：未找到MV播放状态")
        return False

    if not mv_state.get("is_playing", False) and not mv_state.get("isPlaying", False):
        logging.error("✗ 测试失败 - 任务25未完成：MV未在播放")
        return False

    logging.info("✓ 测试通过 - 任务25完成：搜索薛之谦、播放演员、收藏、查看歌词、报告第一句、播放MV")
    return True


if __name__ == "__main__":
    print(check_composite_xuezhiqian_play_favorite_lyrics_mv())
