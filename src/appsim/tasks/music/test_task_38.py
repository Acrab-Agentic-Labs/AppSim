"""
任务38：收藏歌单"国风榜"，并播放"青花瓷"，收藏歌曲，发布评论"真好听"，查看歌曲百科并告诉我曲风是什么
难度：高
类型：复合操作+推理类
"""

import logging
from .verification_functions import read_json_from_device


def check_composite_guofeng_qinghuaci(result=None, device_id=None, backup_dir=None):
    """
    任务38: 验证复合操作
    1. "国风榜"歌单已被收藏
    2. 播放了"青花瓷"
    3. 歌曲被收藏
    4. 发布了评论"真好听"
    5. 查看了歌曲百科
    6. AI回答包含曲风信息"流行-华语流行"
    """
    # 1. 检查"国风榜"是否被收藏
    collected_items = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir)
    if not collected_items:
        logging.error("✗ 测试失败 - 任务38未完成：未找到收藏数据")
        return False

    collected_playlists = collected_items.get("collectedPlaylists", []) or collected_items.get("playlists", [])
    guofeng_collected = any(
        "国风榜" in p.get("playlistName", "") or "国风榜" in p.get("name", "") or p.get("playlistId") == "playlist_009"
        for p in collected_playlists
    )
    if not guofeng_collected:
        logging.error("✗ 测试失败 - 任务38未完成：未收藏'国风榜'歌单")
        return False

    # 2. 检查是否播放了"青花瓷"
    playback_state = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    played_qinghuaci = False
    if playback_state:
        current_song = playback_state.get("currentSong", {})
        if current_song and "青花瓷" in current_song.get("songName", ""):
            played_qinghuaci = True
    if not played_qinghuaci and play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
        for record in records:
            if isinstance(record, dict) and ("青花瓷" in record.get("songName", "") or "青花瓷" in record.get("name", "")):
                played_qinghuaci = True
                break
    if not played_qinghuaci:
        logging.error("✗ 测试失败 - 任务38未完成：未播放'青花瓷'")
        return False

    # 3. 检查歌曲是否被收藏
    favorites = read_json_from_device("autotest/user_favorites.json", device_id, result, backup_dir)
    if not favorites:
        logging.error("✗ 测试失败 - 任务38未完成：未找到收藏数据")
        return False

    favorited_songs = favorites.get("favoriteSongs", []) or favorites.get("songs", [])
    if not any("青花瓷" in song.get("songName", "") or "青花瓷" in song.get("name", "") for song in favorited_songs):
        logging.error("✗ 测试失败 - 任务38未完成：未收藏'青花瓷'")
        return False

    # 4. 检查是否发布了评论"真好听"
    comments = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments:
        logging.error("✗ 测试失败 - 任务38未完成：未找到评论数据")
        return False

    user_comments = comments.get("userComments", []) or comments.get("user_comments", [])
    has_comment = any("真好听" in c.get("content", "") for c in user_comments)
    if not has_comment:
        logging.error("✗ 测试失败 - 任务38未完成：未发布评论'真好听'")
        return False

    # 5. 检查是否查看了歌曲百科
    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state:
        logging.error("✗ 测试失败 - 任务38未完成：未找到应用状态")
        return False

    # 检查currentPage或navigationHistory中是否有song_detail记录
    viewed_song_detail = False
    if app_state.get("currentPage") == "song_detail":
        viewed_song_detail = True
    elif app_state.get("song_detail_viewed", False) or app_state.get("song_encyclopedia_viewed", False):
        viewed_song_detail = True
    else:
        nav_history = app_state.get("navigationHistory", [])
        for record in nav_history:
            page = record.get("page", "") if isinstance(record, dict) else str(record)
            if "song_detail" in page:
                viewed_song_detail = True
                break

    if not viewed_song_detail:
        logging.error("✗ 测试失败 - 任务38未完成：未查看歌曲百科")
        return False

    # 6. 检查AI回答是否包含曲风信息
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务38未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg:
        logging.error("✗ 测试失败 - 任务38未完成：final_message为空")
        return False

    # 检查是否包含曲风关键词
    if "流行" in final_msg or "华语流行" in final_msg or "华语" in final_msg:
        logging.info("✓ 测试通过 - 任务38完成：收藏国风榜、播放青花瓷、收藏、评论、查看百科、报告曲风")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务38未完成：AI未正确报告曲风信息。回答: '{final_msg}'")
        return False


if __name__ == "__main__":
    print(check_composite_guofeng_qinghuaci())
