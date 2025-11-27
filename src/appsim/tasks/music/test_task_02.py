"""
任务2：在‘我的’页面的所有歌单中哪一个歌单里的歌曲数量最多
难度：中
类型：推理类
"""

import logging
import sys
from .verification_functions import read_json_from_device

def find_playlist_with_most_songs(result=None, device_id=None, backup_dir=None):
    """
    任务2: 找出歌曲数量最多的歌单
    - 从 user_playlists.json 找出歌曲最多的歌单
    - 检查AI的 final_message 是否包含该歌单名
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务2未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务2未完成：final_message格式错误: {final_msg}")
        return False

    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir=backup_dir)
    if not data or "playlists" not in data or not data["playlists"]:
        logging.error("✗ 测试失败 - 任务2未完成：无法从设备读取歌单数据或歌单列表为空")
        return False

    # 找到歌曲数量最多的歌单
    playlist_with_most_songs = max(data["playlists"], key=lambda p: p.get("songCount", 0))
    most_songs_playlist_name = playlist_with_most_songs.get("playlistName")

    if not most_songs_playlist_name:
        logging.error("✗ 测试失败 - 任务2未完成：在设备数据中歌曲最多的歌单没有名称")
        return False

    # 检查AI的返回结果
    if most_songs_playlist_name in final_msg:
        logging.info(f"✓ 测试通过 - 任务2完成：AI正确返回了歌曲最多的歌单: {most_songs_playlist_name}")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务2未完成：AI返回错误。正确答案应包含'{most_songs_playlist_name}', 实际返回: '{final_msg}'")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务2：找出歌曲数量最多的歌单")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP，进入'我的'页面")
    print("  2. 查看所有歌单及其歌曲数量")
    print("  3. 找出数量最多的歌单并返回其名称")
    print("\n🔍 开始验证...")

    mock_result = {
        "final_message": "歌曲数量最多的歌单是'热歌榜'。"
    }
    # 注意: 独立运行时，需要一个 autotest/user_playlists.json 文件且其中'热歌榜'歌曲最多
    success = find_playlist_with_most_songs(result=mock_result)

    print(f"\n任务2验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
