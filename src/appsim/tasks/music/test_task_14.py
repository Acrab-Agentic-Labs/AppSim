"""
任务14：搜索一个歌手，进入歌手主页，播放第一首歌
难度：中
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_search_artist_and_play(result=None, device_id=None, backup_dir=None):
    """
    任务14: 验证是否搜索歌手并播放了其歌曲
    - 检查 search_history.json 中是否有 resultType 为 'artist' 的记录
    - 确保该记录的 action 为 'play'
    """
    data = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir=backup_dir)

    if data and "searches" in data:
        for search in data["searches"]:
            if search.get("resultType") == "artist" and search.get("action") == "play":
                query = search.get("query", "未知歌手")
                logging.info(f"✓ 测试通过 - 任务14完成：在搜索历史中找到播放歌手'{query}'歌曲的记录")
                return True

    logging.error("✗ 测试失败 - 任务14未完成：未在搜索历史中找到播放歌手歌曲的记录")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务14：搜索一个歌手，进入歌手主页，播放第一首歌")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击搜索按钮并输入歌手名称")
    print("  3. 点击搜索结果中的歌手，进入歌手主页")
    print("  4. 在歌手主页中点击第一首歌曲播放")
    print("\n🔍 开始验证...")

    success = check_search_artist_and_play()

    print(f"\n任务14验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
