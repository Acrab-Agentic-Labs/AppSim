
"""
任务30：搜索一位歌手，进入歌手主页播放一个MV
难度：高

人工操作步骤：
  1. 打开音乐APP
  2. 点击搜索按钮
  3. 输入歌手名称
  4. 点击搜索结果中的歌手，进入歌手主页
  5. 在歌手主页找到MV列表或MV选项卡
  6. 选择一个MV并播放

验证标准：
调用task_30_check_play_mv函数进行验证
检查mv_playback.json中currentMV.mvId是否为指定MV且isPlaying为true
"""

import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .verification_functions import task_30_check_play_mv


def test30(mv_id=None, result=None, device_id=None):
    if mv_id is None:
        logging.warning("未指定mv_id，将验证是否有任何MV正在播放")

    result1 = task_30_check_play_mv(mv_id=mv_id, device_id=device_id, result=result)

    if result1:
        logging.debug("✓ 测试通过 - 任务30完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务30未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务30：搜索一位歌手，进入歌手主页播放一个MV")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击搜索按钮")
    print("  3. 输入歌手名称")
    print("  4. 点击搜索结果中的歌手，进入歌手主页")
    print("  5. 在歌手主页找到MV列表或MV选项卡")
    print("  6. 选择一个MV并播放")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    mv_id = args[0] if args else None
    success = test30(mv_id=mv_id)

    print(f"任务30验证结果: {success}")
    sys.exit(0 if success else 1)
