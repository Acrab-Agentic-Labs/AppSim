"""
任务35：搜索'倔强'并播放，收藏该歌曲，查看歌词并告诉我第一句，更改播放器样式，然后创建一个新歌单并添加该歌曲
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device


def check_composite_juejiang_full(result=None, device_id=None, backup_dir=None):
    """
    任务35: 验证复合操作
    1. 搜索历史包含"倔强"
    2. 歌曲被收藏
    3. 歌词已显示
    4. AI回答包含第一句歌词"当我和世界不一样"
    5. 播放器样式已更改
    6. 新歌单已创建并添加了歌曲
    """
    # 1. 检查搜索历史
    search_history = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir)
    if not search_history:
        logging.error("✗ 测试失败 - 任务35未完成：未找到搜索历史")
        return False

    searched = False
    for search in search_history.get("searches", []):
        if "倔强" in search.get("query", ""):
            searched = True
            break
    if not searched:
        logging.error("✗ 测试失败 - 任务35未完成：未搜索'倔强'")
        return False

    # 2. 检查歌曲是否被收藏
    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        logging.error("✗ 测试失败 - 任务35未完成：未找到收藏数据")
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("倔强" in song.get("songName", "") or "倔强" in song.get("name", "") for song in favorited_songs):
        logging.error("✗ 测试失败 - 任务35未完成：未收藏'倔强'")
        return False

    # 3. 检查歌词是否已显示
    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state:
        logging.error("✗ 测试失败 - 任务35未完成：未找到应用状态")
        return False

    if not app_state.get("lyrics_shown", False) and not app_state.get("showLyrics", False):
        logging.error("✗ 测试失败 - 任务35未完成：未查看歌词")
        return False

    # 4. 检查AI回答是否包含第一句歌词
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务35未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or "当我和世界不一样" not in final_msg:
        logging.error(f"✗ 测试失败 - 任务35未完成：AI未正确报告第一句歌词。回答: '{final_msg}'")
        return False

    # 5. 检查播放器样式是否已更改
    player_settings = read_json_from_device("autotest/player_settings.json", device_id, result, backup_dir)
    if not player_settings:
        logging.error("✗ 测试失败 - 任务35未完成：未找到播放器设置")
        return False

    if not player_settings.get("style_changed", False):
        logging.error("✗ 测试失败 - 任务35未完成：未更改播放器样式")
        return False

    # 6. 检查新歌单是否已创建并添加歌曲
    user_playlists = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)
    if not user_playlists:
        logging.error("✗ 测试失败 - 任务35未完成：未找到歌单数据")
        return False

    playlists = user_playlists.get("playlists", [])
    if len(playlists) == 0:
        logging.error("✗ 测试失败 - 任务35未完成：未创建新歌单")
        return False

    # 检查最新歌单是否有歌曲
    latest_playlist = playlists[-1]
    song_count = latest_playlist.get("songCount", 0)
    song_ids = latest_playlist.get("songIds", []) or latest_playlist.get("songs", [])
    if song_count == 0 and len(song_ids) == 0:
        logging.error("✗ 测试失败 - 任务35未完成：新歌单中未添加歌曲")
        return False

    logging.info("✓ 测试通过 - 任务35完成：搜索倔强、播放、收藏、查看歌词、报告第一句、更改样式、创建歌单")
    return True


if __name__ == "__main__":
    print(check_composite_juejiang_full())
