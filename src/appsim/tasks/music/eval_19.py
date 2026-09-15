"""
任务19：在排行榜中打开一个榜单并播放第一首歌曲
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

# 根据 playlists.json 定义所有属于“排行榜”性质的歌单名称
RANKING_PLAYLIST_NAMES = [
    "热歌榜", "新歌榜", "国风榜", "ACG榜", "日语榜",
    "飙升榜", "硬地原创音乐榜", "潮流风向榜"
]

def _load_rank_list_song_ids(device_id=None, result=None, backup_dir=None):
    playlists_data = read_json_from_device("playlists.json", device_id, result, backup_dir)
    if not playlists_data:
        logging.error("✗ 测试失败 - 任务19未完成：无法从设备读取歌单数据(playlists.json)")
        return None

    rank_list_song_ids = set()
    for playlist in playlists_data:
        if playlist.get("playlistName") in RANKING_PLAYLIST_NAMES:
            if playlist.get("songIds") and isinstance(playlist["songIds"], list):
                rank_list_song_ids.update(playlist["songIds"])

    if not rank_list_song_ids:
        logging.error("✗ 测试失败 - 任务19未完成：在设备数据中未找到任何已定义的排行榜歌单或歌单均为空")
        return None

    logging.info(f"  → 已从设备加载 {len(rank_list_song_ids)} 首排行榜歌曲ID用于验证")
    return rank_list_song_ids


def _get_latest_played_song_id(device_id=None, result=None, backup_dir=None):
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir)
    if play_records is None:
        logging.warning("  → 未能读取播放记录(play_records.json)，尝试使用当前播放状态兜底")
    elif not isinstance(play_records, list):
        logging.warning(f"  → 播放记录格式异常，应为list，实际为: {type(play_records).__name__}")
    elif not play_records:
        logging.warning("  → 播放记录为空，尝试使用当前播放状态兜底")
    else:
        latest_play = play_records[-1]
        played_song_id = latest_play.get("songId")
        if played_song_id:
            logging.info(f"  → 最新播放的歌曲ID是: '{played_song_id}'")
            return played_song_id
        logging.warning(f"  → 最新播放记录中没有找到'songId': {latest_play}")

    playback_state = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir)
    current_song = playback_state.get("currentSong") if playback_state else None
    played_song_id = current_song.get("songId") if current_song else None
    if played_song_id:
        logging.info(f"  → 使用当前播放状态中的歌曲ID兜底: '{played_song_id}'")
    return played_song_id


def verify_ranked_song_played(result=None, device_id=None, backup_dir=None):
    """
    任务19: 验证是否播放了排行榜的歌曲
    - 读取 play_records.json 获取最新的播放记录
    - 读取 playlists.json 获取所有排行榜歌单的歌曲ID集合
    - 验证最新播放的歌曲ID是否存在于排行榜歌单的歌曲ID集合中
    """
    rank_list_song_ids = _load_rank_list_song_ids(device_id, result, backup_dir)
    if not rank_list_song_ids:
        return False

    played_song_id = _get_latest_played_song_id(device_id, result, backup_dir)
    if not played_song_id:
        logging.error("✗ 测试失败 - 任务19未完成：无法从播放记录或当前播放状态中获取歌曲ID")
        return False

    if played_song_id in rank_list_song_ids:
        logging.info(f"✓ 测试通过 - 任务19完成：播放的歌曲'{played_song_id}'确实存在于排行榜歌单中。")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务19未完成：播放的歌曲'{played_song_id}'不属于任何一个已定义的排行榜歌单。")
        return False

if __name__ == "__main__":

    print(verify_ranked_song_played())
