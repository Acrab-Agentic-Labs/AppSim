"""
任务14：搜索一个歌手，进入歌手主页，播放第一首歌
难度：中

人工操作步骤：
  1. 打开音乐APP
  2. 点击搜索按钮
  3. 输入歌手名称
  4. 点击搜索结果中的歌手，进入歌手主页
  5. 在歌手主页中点击第一首歌曲播放

验证标准：
调用task_14_check_search_artist_and_play函数进行验证
检查search_history.json中是否有歌手搜索并播放的记录(resultType="artist", action="play")
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_14_check_search_artist_and_play(device_id=None, result=None, backup_dir=None):
    """
    任务14: 搜索某个歌手并播放其中的第一首歌
    验证: 检查search_history.json中有歌手搜索记录,且resultType为"artist",action为"play"
    """
    data = read_json_from_device("autotest/search_history.json", device_id, result, backup_dir=backup_dir)
    if data and "searches" in data:
        for search in data["searches"]:
            if search.get("resultType") == "artist" and search.get("action") == "play":
                return True
    return False


def test(result=None, device_id=None, backup_dir=None):
    result1 = task_14_check_search_artist_and_play(device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug("✓ 测试通过 - 任务14完成")
        return True
    else:
        logging.debug("✗ 测试失败 - 任务14未完成")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务14：搜索一个歌手，进入歌手主页，播放第一首歌")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 打开音乐APP")
    print("  2. 点击搜索按钮")
    print("  3. 输入歌手名称")
    print("  4. 点击搜索结果中的歌手，进入歌手主页")
    print("  5. 在歌手主页中点击第一首歌曲播放")
    print("\n🔍 开始验证...")

    # 从命令行获取参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    success = test(*args)

    print(f"任务14验证结果: {success}")
    sys.exit(0 if success else 1)