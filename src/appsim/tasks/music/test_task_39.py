"""
任务39：收藏歌单"ACG榜"，并播放"夜曲"，收藏歌曲，查看歌词并告诉我第一句歌词是什么，然后查看一下这周的听歌时长
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device


def check_composite_acg_yequ(result=None, device_id=None, backup_dir=None):
    """
    任务39: 验证复合操作
    1. "ACG榜"歌单已被收藏
    2. 播放了"夜曲"
    3. 歌曲被收藏
    4. 歌词已显示
    5. AI回答包含第一句歌词"我在弹奏萧邦的夜曲"
    6. 查看了听歌时长统计
    """
    # 1. 检查"ACG榜"是否被收藏
    collected_items = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir)
    if not collected_items:
        logging.error("✗ 测试失败 - 任务39未完成：未找到收藏数据")
        return False

    collected_playlists = collected_items.get("collectedPlaylists", []) or collected_items.get("playlists", [])
    acg_collected = any(
        "ACG榜" in p.get("playlistName", "") or "ACG榜" in p.get("name", "") or p.get("playlistId") == "playlist_010"
        for p in collected_playlists
    )
    if not acg_collected:
        logging.error("✗ 测试失败 - 任务39未完成：未收藏'ACG榜'歌单")
        return False

    # 2. 检查是否播放了"夜曲"
    playback_state = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    played_yequ = False
    if playback_state:
        current_song = playback_state.get("currentSong", {})
        if current_song and "夜曲" in current_song.get("songName", ""):
            played_yequ = True
    if not played_yequ and play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
        for record in records:
            if isinstance(record, dict) and ("夜曲" in record.get("songName", "") or "夜曲" in record.get("name", "")):
                played_yequ = True
                break
    if not played_yequ:
        logging.error("✗ 测试失败 - 任务39未完成：未播放'夜曲'")
        return False

    # 3. 检查歌曲是否被收藏
    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        logging.error("✗ 测试失败 - 任务39未完成：未找到收藏数据")
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("夜曲" in song.get("songName", "") or "夜曲" in song.get("name", "") for song in favorited_songs):
        logging.error("✗ 测试失败 - 任务39未完成：未收藏'夜曲'")
        return False

    # 4. 检查歌词是否已显示
    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state:
        logging.error("✗ 测试失败 - 任务39未完成：未找到应用状态")
        return False

    if not app_state.get("lyrics_shown", False) and not app_state.get("showLyrics", False):
        logging.error("✗ 测试失败 - 任务39未完成：未查看歌词")
        return False

    # 5. 检查AI回答是否包含第一句歌词
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务39未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or "我在弹奏萧邦的夜曲" not in final_msg:
        # 也尝试匹配可能的变体
        if not final_msg or ("萧邦" not in final_msg and "夜曲" not in final_msg):
            logging.error(f"✗ 测试失败 - 任务39未完成：AI未正确报告第一句歌词。回答: '{final_msg}'")
            return False

    # 6. 检查是否查看了听歌时长统计
    if not app_state.get("listening_stats_viewed", False):
        logging.error("✗ 测试失败 - 任务39未完成：未查看听歌时长统计")
        return False

    logging.info("✓ 测试通过 - 任务39完成：收藏ACG榜、播放夜曲、收藏、查看歌词、报告第一句、查看时长")
    return True


if __name__ == "__main__":
    print(check_composite_acg_yequ())
