"""
任务19：在排行榜中打开一个榜单并播放第一首歌曲
难度：中

人工操作步骤：
  1. 打开音乐APP
  2. 进入"排行榜"页面
  3. 选择任意一个榜单
  4. 点击第一首歌曲播放

验证标准：
调用task_19_check_rank_list_play函数进行验证
检查playback_state.json中currentSong.source是否包含"rank"或"榜单"
"""

import logging
import sys
from .verification_functions import task_19_check_play_from_billboard


def test19(result=None, device_id=None, backup_dir=None):
    result1 = task_19_check_rank_list_play(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务19完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务19未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务19：在排行榜中打开一个榜单并播放第一首歌曲")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 进入'排行榜'页面")
    print("  3. 选择任意一个榜单")
    print("  4. 点击第一首歌曲播放")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test19(*args)

    print(f"任务19验证结果: {success}")
    sys.exit(0 if success else 1)
