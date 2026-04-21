"""
任务29：将关注列表中的一位关注人删除
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_artist_is_unfollowed(result=None, device_id=None, backup_dir=None):
    """
    任务29: 验证是否已取消关注
    - 检查 followed_artists.json 中的 recentUnfollowedArtist 字段是否存在且不为空
    - 这是一个简化的验证，只检查最近有取消关注的行为发生。
    """
    data = read_json_from_device("autotest/followed_artists.json", device_id, result, backup_dir)

    if data and "recentUnfollowedArtist" in data and data["recentUnfollowedArtist"]:
        artist_id = data["recentUnfollowedArtist"]
        logging.info(f"✓ 测试通过 - 任务29完成：检测到最近有取消关注行为，艺术家ID: {artist_id}")
        return True
    else:
        logging.error("✗ 测试失败 - 任务29未完成：未在设备状态中检测到取消关注的记录")
        return False

if __name__ == "__main__":

    print(check_artist_is_unfollowed())
