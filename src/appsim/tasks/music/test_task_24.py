"""
任务24：在歌单中选择一首歌曲并发表评论
难度：高
"""

import logging
import sys
from .verification_functions import read_json_from_device

def check_comment_is_posted(result=None, device_id=None, backup_dir=None):
    """
    任务24: 验证是否成功发表了评论
    - 检查 comments.json 中 userComments 列表是否不为空
    - 验证最新一条评论包含 songId 和 content
    """
    data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)

    if (data and "userComments" in data and
            isinstance(data["userComments"], list) and len(data["userComments"]) > 0):
        latest_comment = data["userComments"][-1]
        if "songId" in latest_comment and "content" in latest_comment:
            song_id = latest_comment['songId']
            content = latest_comment['content']
            logging.info(f"✓ 测试通过 - 任务24完成：检测到新评论。歌曲ID: {song_id}, 内容: '{content}'")
            return True

    logging.error("✗ 测试失败 - 任务24未完成：未在设备上找到用户发表的有效评论")
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    print("=" * 70)
    print("任务24：在歌单中选择一首歌曲并发表评论")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入任意歌曲的播放或详情页面")
    print("  2. 滑动到评论区，点击'发表评论'")
    print("  3. 输入评论内容并点击'发表'")
    print("\n🔍 开始验证...")

    success = check_comment_is_posted()

    print(f"\n任务24验证结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
