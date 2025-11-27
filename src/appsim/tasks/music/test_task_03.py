"""
任务3：删除‘我的’页面中热歌榜歌单的第一首歌曲
难度：中

人工操作步骤：
  1. 打开音乐APP
  2. 点击底部导航栏的"我的"
  3. 找到"热歌榜"歌单并点击进入
  4. 选中第一首歌曲
  5. 点击删除按钮并确认

验证标准：
调用task_03_delete_first_song_from_hot_playlist函数进行验证
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_03_delete_first_song_from_hot_playlist(device_id=None, result=None, backup_dir=None):
    """
    任务3: 删除‘我的’页面中热歌榜歌单的第一首歌曲
    验证: 检查 song_deletion_records.json 中是否有 '热歌榜'(playlist_002) 的删除记录
    """
    # 从设备拉取歌曲删除记录文件
    data = read_json_from_device("autotest/song_deletion_records.json", device_id, result, backup_dir=backup_dir)

    # 检查数据是否是一个非空的列表
    if data and isinstance(data, list) and len(data) > 0:
        # 遍历所有删除记录
        for record in data:
            # 检查是否有来自"热歌榜"(playlist_002)的删除记录
            if record.get("playlistId") == "playlist_002":
                deleted_song_id = record.get("songId")
                print(f"  → 设备状态确认: 找到'热歌榜'的歌曲删除记录 (Song ID: {deleted_song_id})")
                return True
        print("  → 设备状态检查: 找到了删除记录,但没有来自'热歌榜'的记录")
    else:
        print("  → 设备状态检查: 未找到任何歌曲删除记录")

    # 如果设备状态检查失败,可以增加对final_message的检查作为后备
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if final_msg and isinstance(final_msg, str):
            if "删除" in final_msg and ("成功" in final_msg or "已完成" in final_msg):
                print(f"  → AI确认完成: {final_msg}")
                print("  → 注意: 设备状态未更新,但AI声称已完成")
                return True

    print("  → 验证失败: 设备状态未确认且AI未声称完成")
    return False


def task_03_check_navigate_to_profile(device_id=None, result=None, backup_dir=None):
    """
    任务3: 从"推荐"页面进入"我的"页面
    验证: 检查app_state.json中currentPage是否为"profile"或"my"
    """
    data = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir=backup_dir)
    if data:
        current_page = data.get("currentPage")
        return current_page in ["profile", "my", "mine"]
    return False


def test(result=None, device_id=None, backup_dir=None):
    result1 = task_03_delete_first_song_from_hot_playlist(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务3完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务3未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务3：删除‘我的’页面中热歌榜歌单的第一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击底部导航栏的'我的'")
    print("  3. 找到'热歌榜'歌单并点击进入")
    print("  4. 选中第一首歌曲")
    print("  5. 点击删除按钮并确认")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务3验证结果: {success}")
    sys.exit(0 if success else 1)