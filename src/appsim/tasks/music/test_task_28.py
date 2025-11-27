"""
任务28：搜索一个歌手,在歌手主页选择一个专辑并收藏
难度：高

人工操作步骤：
  1. 搜索歌手
  2. 进入歌手页面
  3. 选择专辑
  4. 收藏

验证标准：
调用task_28_check_collect_album函数进行验证

参数：album_id，默认自动检测最新收藏
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_28_check_collect_album(album_id, device_id=None, result=None, backup_dir=None):
    """
    任务28: 搜索一个歌手,在歌手主页选择一个专辑并收藏
    验证: 检查collected_items.json中collectedAlbums是否包含指定专辑
    :param album_id: 收藏的专辑ID
    """
    data = read_json_from_device("autotest/collected_items.json", device_id, result, backup_dir=backup_dir)
    if data and "collectedAlbums" in data:
        album_ids = [a.get("albumId") for a in data["collectedAlbums"]]
        return album_id in album_ids
    return False


def test(album_id=None, result=None, device_id=None, backup_dir=None):
    # 如果没有指定album_id，自动从collected_items.json获取最新收藏的专辑
    if album_id is None:
        collected_data = read_json_from_device("autotest/collected_items.json", device_id=device_id, result=result, backup_dir=backup_dir)

        if collected_data and "collectedAlbums" in collected_data and collected_data["collectedAlbums"]:
            # 获取最后一个（最新）收藏的专辑
            latest_album = collected_data["collectedAlbums"][-1]
            album_id = latest_album.get("albumId")
        else:
            logging.debug("✗ 错误：无法检测到已收藏的专辑")
            return False

    result1 = task_28_check_collect_album(album_id, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug(f"✓ 测试通过 - 专辑 {album_id} 已成功收藏")
        return True
    else:
        logging.debug(f"✗ 测试失败 - 专辑 {album_id} 未在收藏列表中")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务28：搜索一个歌手,在歌手主页选择一个专辑并收藏")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 搜索歌手")
    print("  2. 进入歌手页面")
    print("  3. 选择专辑")
    print("  4. 收藏")

    # 可以通过命令行参数传入album_id
    # 用法1：python test_task_28.py          # 自动检测最新收藏
    # 用法2：python test_task_28.py album_002  # 手动指定专辑ID
    album_id = sys.argv[1] if len(sys.argv) > 1 else None
    success = test(album_id=album_id)

    print(f"任务28验证结果: {success}")
    sys.exit(0 if success else 1)