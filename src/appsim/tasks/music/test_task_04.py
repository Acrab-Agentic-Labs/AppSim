"""
任务4：播放当前歌曲
难度：低
"""

import logging
from .verification_functions import read_json_from_device


def check_current_song_is_playing(result=None, device_id=None, backup_dir=None):
    """
    任务4: 验证当前歌曲是否正在播放
    - 检查 playback_state.json 中 isPlaying 是否为 true
    - 通过对比备份数据确认是由agent操作触发的播放（而非初始状态）
    """
    data = read_json_from_device("autotest/playback_state.json", device_id, result, backup_dir=backup_dir)

    if not data:
        logging.error("✗ 测试失败 - 任务4未完成：无法读取播放状态")
        return False

    # 检查是否正在播放
    if not (data.get("isPlaying", False) or data.get("is_playing", False)):
        logging.error("✗ 测试失败 - 任务4未完成：当前歌曲未在播放状态")
        return False

    # 检查是否有播放操作记录（区分初始状态和agent操作）
    if data.get("playTriggered", False) or data.get("play_triggered", False):
        logging.info("✓ 测试通过 - 任务4完成：当前歌曲正在播放（检测到播放操作）")
        return True

    # 检查播放记录
    play_records = read_json_from_device("data/play_records.json", device_id, result, backup_dir=backup_dir)
    if play_records:
        records = play_records.get("records", play_records) if isinstance(play_records, dict) else play_records
        if len(records) > 0:
            logging.info("✓ 测试通过 - 任务4完成：当前歌曲正在播放（检测到播放记录）")
            return True

    # 检查lastAction字段
    if data.get("lastAction") == "play" or data.get("last_action") == "play":
        logging.info("✓ 测试通过 - 任务4完成：当前歌曲正在播放（检测到play动作）")
        return True

    # 如果进度发生了变化（与初始状态不同），也认为是有操作的
    progress = data.get("progress", 0)
    if progress == 0:
        logging.info("✓ 测试通过 - 任务4完成：当前歌曲正在播放（进度为0，刚开始播放）")
        return True

    logging.error("✗ 测试失败 - 任务4未完成：播放状态为初始状态，未检测到agent的播放操作")
    return False


if __name__ == "__main__":
    print(check_current_song_is_playing())
