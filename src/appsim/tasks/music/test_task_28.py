"""
任务28：搜索一个歌手,在歌手主页选择一个专辑并收藏
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_album_is_collected(result=None, device_id=None, backup_dir=None):
    """
    任务28: 验证专辑是否被收藏
    - 从 app_state.json 获取当前查看的专辑ID
    - 检查该ID是否存在于 collected_items.json 的 collectedAlbums 列表中
    """
    # 首先获取当前正在查看的专辑ID
    app_state = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir)
    if not app_state or not app_state.get("currentAlbumId"):
        logging.error("✗ 测试失败 - 任务28未完成：无法从设备状态确定当前查看的专辑ID")
        return False
    current_album_id = app_state["currentAlbumId"]
    logging.info(f"  → 当前查看的专辑ID为: {current_album_id}")

    # 然后检查收藏列表
    collected_data = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir)
    if not collected_data or "collectedAlbums" not in collected_data or not isinstance(collected_data.get("collectedAlbums"), list):
        logging.error("✗ 测试失败 - 任务28未完成：无法从设备读取收藏列表或数据格式不正确")
        return False

    album_ids = [a.get("albumId") for a in collected_data["collectedAlbums"]]
    if current_album_id in album_ids:
        logging.info(f"✓ 测试通过 - 任务28完成：专辑 {current_album_id} 已成功收藏")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务28未完成：专辑 {current_album_id} 未在收藏列表中找到")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务28：搜索一个歌手,在歌手主页选择一个专辑并收藏")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 搜索一位歌手并进入其主页")
    print("  2. 切换到'专辑'标签页")
    print("  3. 进入任意一个专辑的详情页")
    print("  4. 点击收藏按钮")
    print("\n🔍 开始验证...")

    success = check_album_is_collected()

    print(f"\n任务28验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
