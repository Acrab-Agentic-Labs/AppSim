



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
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .verification_functions import read_json_from_device, task_15_check_view_song_detail


def test15(song_id=None, result=None, device_id=None):
    # 如果没有指定song_id，自动从app_state.json获取当前查看的歌曲详情
    if song_id is None:
        app_state = read_json_from_device("autotest/app_state.json", device_id=device_id, result=result)

        if app_state and app_state.get("currentPage") == "song_detail" and app_state.get("currentSongId"):
            song_id = app_state.get("currentSongId")
        else:
            logging.debug("✗ 错误：无法检测到当前查看的歌曲详情")
            return False

    result1 = task_15_check_view_song_detail(song_id, device_id=device_id, result=result)

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
    success = test15(song_id=song_id)

    print(f"任务15验证结果: {success}")
    sys.exit(0 if success else 1)
