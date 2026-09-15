"""
任务29：将关注列表中的一位关注人删除
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def _has_unfollow_action(record):
    if not isinstance(record, dict):
        return False

    action_values = [record.get(key) for key in ["action", "type", "event", "operation"]]
    normalized_values = {str(value).strip().lower().replace("-", "_").replace(" ", "_") for value in action_values if value}
    return bool({"unfollow", "remove_follow", "unfollow_artist", "取消关注"} & normalized_values) or any(
        "取消关注" in value for value in normalized_values
    )


def verify_artist_unfollowed(result=None, device_id=None, backup_dir=None):
    """
    任务29: 验证是否已取消关注
    - 检查 followed_artists.json 中是否存在取消关注行为记录
    """
    data = read_json_from_device("autotest/followed_artists.json", device_id, result, backup_dir)

    if not data:
        logging.error("✗ 测试失败 - 任务29未完成：无法读取关注歌手状态")
        return False

    single_value_keys = ["recentUnfollowedArtist", "recentUnfollowedArtistId", "lastUnfollowedArtist", "lastUnfollowedArtistId", "recentlyUnfollowed"]
    for key in single_value_keys:
        if data.get(key):
            logging.info(f"✓ 测试通过 - 任务29完成：检测到取消关注记录 {key}={data[key]}")
            return True

    list_keys = ["unfollowedArtists", "unfollowRecords"]
    for key in list_keys:
        value = data.get(key)
        if isinstance(value, list) and value:
            logging.info(f"✓ 测试通过 - 任务29完成：检测到取消关注记录 {key}")
            return True

    action_list_keys = ["recentActions", "actions", "actionRecords"]
    for key in action_list_keys:
        value = data.get(key)
        if isinstance(value, list) and any(_has_unfollow_action(item) for item in value[-5:]):
            logging.info(f"✓ 测试通过 - 任务29完成：动作记录中检测到取消关注行为 {key}")
            return True

    if _has_unfollow_action(data):
        logging.info("✓ 测试通过 - 任务29完成：状态中检测到取消关注行为")
        return True

    logging.error(f"✗ 测试失败 - 任务29未完成：未在设备状态中检测到取消关注的记录。当前状态: {data}")
    return False

if __name__ == "__main__":

    print(verify_artist_unfollowed())
