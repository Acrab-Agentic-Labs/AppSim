"""
任务27：更改歌单的排序顺序
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_playlist_sort_order_is_changed(result=None, device_id=None, backup_dir=None):
    """
    任务27: 验证歌单的排序顺序是否已更改
    - 从 user_playlists.json 获取当前正在查看的歌单ID
    - 检查该歌单的 sortOrder 字段是否不是默认值（例如 'default' 或 null）
    """
    data = read_json_from_device("autotest/user_playlists.json", device_id, result, backup_dir)

    if not data or not data.get("currentViewingPlaylist") or not data.get("playlists"):
        logging.error("✗ 测试失败 - 任务27未完成：无法获取当前歌单信息")
        return False
    
    current_playlist_id = data.get("currentViewingPlaylist")
    
    for playlist in data["playlists"]:
        if playlist.get("playlistId") == current_playlist_id:
            sort_order = playlist.get("sortOrder", "default") # 假设'default'是初始值
            if sort_order != "default":
                logging.info(f"✓ 测试通过 - 任务27完成：歌单 {current_playlist_id} 的排序顺序已更改为 '{sort_order}'")
                return True
            else:
                logging.error(f"✗ 测试失败 - 任务27未完成：歌单 {current_playlist_id} 的排序顺序仍为默认值")
                return False

    logging.error(f"✗ 测试失败 - 任务27未完成：在数据中未找到当前查看的歌单 {current_playlist_id}")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务27：更改歌单的排序顺序")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入任意一个歌单")
    print("  2. 点击排序按钮（例如，按添加时间、按歌曲名等）")
    print("  3. 选择一个新的排序方式")
    print("\n🔍 开始验证...")

    success = check_playlist_sort_order_is_changed()

    print(f"\n任务27验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
