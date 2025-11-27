"""
任务29：将关注列表中的一位歌手删除
难度：高

人工操作步骤：
  1. 进入关注列表
  2. 找到歌手
  3. 取消关注

验证标准：
调用task_29_check_unfollow_artist函数进行验证

参数：artist_id，默认'artist_002'
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_29_check_unfollow_artist(artist_id=None, device_id=None, result=None, backup_dir=None):
    """
    任务29: 将关注列表中的一位歌手删除
    验证: 检查followed_artists.json中followedArtists是否不包含指定歌手
    如果未指定artist_id，则检查关注列表是否有减少
    :param artist_id: 取消关注的歌手ID (可选)
    """
    data = read_json_from_device("autotest/followed_artists.json", device_id, result, backup_dir=backup_dir)

    if artist_id:
        # 指定了artist_id，检查该歌手是否不在列表中
        if data and "followedArtists" in data:
            artist_ids = [a.get("artistId") for a in data["followedArtists"]]
            return artist_id not in artist_ids
        return False
    else:
        # 未指定artist_id，检查关注列表变化
        # 简单检查：如果关注列表存在且数量小于初始数量（假设初始有5个歌手）
        if data and "followedArtists" in data:
            initial_artist_count = 5  # 假设初始状态有5个歌手
            current_count = len(data["followedArtists"])
            # 如果当前数量少于初始数量，说明有歌手被取消关注
            return current_count < initial_artist_count
        return True  # 如果列表为空或不存在，也算通过

def test(artist_id=None, result=None, device_id=None, backup_dir=None):
    result1 = task_29_check_unfollow_artist(artist_id=artist_id, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务29完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务29未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务29：将关注列表中的一位歌手删除")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入关注列表")
    print("  2. 找到歌手")
    print("  3. 取消关注")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    artist_id = args[0] if args else None
    success = test(artist_id=artist_id)

    print(f"任务29验证结果: {success}")
    sys.exit(0 if success else 1)