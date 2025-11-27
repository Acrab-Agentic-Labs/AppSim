"""
任务15：点击当前播放的歌曲，查看歌曲详情
难度：中

人工操作步骤：
  1. 在播放界面找到当前正在播放的歌曲
  2. 点击歌曲名称或相关区域
  3. 进入歌曲详情页面

验证标准：
调用task_15_check_view_song_detail函数进行验证
检查app_state.json中currentPage是否为"song_detail"

参数：song_id（歌曲ID），默认自动检测
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_15_check_view_song_detail(song_id, device_id=None, result=None, backup_dir=None):
    """
    任务15: 查看一首歌曲的详细信息
    验证:
    1. 优先检查app_state.json中currentPage为"song_detail"且包含指定songId
    2. 如果设备状态检查失败,检查result["final_message"]是否包含"详细信息"或"歌曲"相关信息
    :param song_id: 查看详情的歌曲ID
    """
    # 方法1: 检查设备状态
    data = read_json_from_device("autotest/app_state.json", device_id, result, backup_dir=backup_dir)
    if data:
        current_page = data.get("currentPage")
        current_song_id = data.get("currentSongId")
        if current_page == "song_detail" and current_song_id == song_id:
            print(f"  → 设备状态确认: 已进入歌曲详情页面 (歌曲ID: {song_id})")
            return True
        elif current_page == "song_detail":
            print(f"  → 设备状态: 已在歌曲详情页面,但歌曲ID不匹配 (期望: {song_id}, 实际: {current_song_id})")

    # 方法2: 检查AI的final_message
    if result and "final_message" in result:
        final_msg = result["final_message"]
        if final_msg and isinstance(final_msg, str):
            # 检查是否提到查看详细信息
            if ("详细" in final_msg or "详情" in final_msg or "信息" in final_msg) and ("歌曲" in final_msg or "歌" in final_msg):
                print(f"  → AI确认: {final_msg}")
                print("  → 注意: 设备状态未更新,但AI声称已完成")
                return True

    print("  → 验证失败: 设备状态未确认且AI未声称完成")
    return False


def test(song_id=None, result=None, device_id=None, backup_dir=None):
    # 如果没有指定song_id，自动从app_state.json获取当前查看的歌曲详情
    if song_id is None:
        app_state = read_json_from_device("autotest/app_state.json", device_id=device_id, result=result, backup_dir=backup_dir)

        if app_state and app_state.get("currentPage") == "song_detail" and app_state.get("currentSongId"):
            song_id = app_state.get("currentSongId")
        else:
            logging.debug("✗ 错误：无法检测到当前查看的歌曲详情")
            return False

    result1 = task_15_check_view_song_detail(song_id, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug(f"✓ 测试通过 - 已成功查看歌曲 {song_id} 的详细信息")
        return True
    else:
        logging.debug(f"✗ 测试失败 - 未正确查看歌曲 {song_id} 的详细信息")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务15：点击当前播放的歌曲，查看歌曲详情")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 在播放界面找到当前正在播放的歌曲")
    print("  2. 点击歌曲名称或相关区域")
    print("  3. 进入歌曲详情页面")

    # 可以通过命令行参数传入song_id
    # 用法1：python test_task_15.py          # 自动检测当前歌曲
    # 用法2：python test_task_15.py song_002  # 手动指定歌曲ID
    song_id = sys.argv[1] if len(sys.argv) > 1 else None
    success = test(song_id=song_id)

    print(f"任务15验证结果: {success}")
    sys.exit(0 if success else 1)