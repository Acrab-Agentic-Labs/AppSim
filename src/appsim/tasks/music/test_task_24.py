"""
任务24：在歌单中选择一首歌曲并发表评论
难度：高

人工操作步骤：
  1. 进入歌曲
  2. 点击评论区
  3. 输入评论
  4. 发表

验证标准：
调用task_24_check_post_comment函数进行验证

参数：song_id, comment_content（可选），默认自动检测最新评论
"""

import logging
import sys
from .verification_functions import read_json_from_device


def task_24_check_post_comment(song_id, comment_content, device_id=None, result=None, backup_dir=None):
    """
    任务24: 在歌单中选择一首歌曲并发表评论
    验证: 检查comments.json中是否有对应歌曲的评论
    :param song_id: 评论的歌曲ID
    :param comment_content: 评论内容(可选,用于精确匹配)
    """
    data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir=backup_dir)
    if data and "userComments" in data:
        for comment in data["userComments"]:
            if comment.get("songId") == song_id:
                if comment_content:
                    return comment.get("content") == comment_content
                return True
    return False


def test(song_id=None, comment_content=None, result=None, device_id=None, backup_dir=None):
    # 如果没有指定song_id，自动从comments.json获取最新发表的评论
    if song_id is None:
        comments_data = read_json_from_device("autotest/comments.json", device_id=device_id, result=result, backup_dir=backup_dir)

        if comments_data and "userComments" in comments_data and comments_data["userComments"]:
            # 获取最后一个（最新）评论
            latest_comment = comments_data["userComments"][-1]
            song_id = latest_comment.get("songId")
        else:
            logging.debug("✗ 错误：无法检测到已发表的评论")
            return False

    result1 = task_24_check_post_comment(song_id, comment_content, device_id=device_id, result=result, backup_dir=backup_dir)

    if result1:
        logging.debug(f"✓ 测试通过 - 已成功为歌曲 {song_id} 发表评论")
        return True
    else:
        logging.debug(f"✗ 测试失败 - 歌曲 {song_id} 未找到评论")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("任务24：在歌单中选择一首歌曲并发表评论")
    print("=" * 70)
    print("\n📋 人工操作步骤：")
    print("  1. 进入歌曲")
    print("  2. 点击评论区")
    print("  3. 输入评论")
    print("  4. 发表")

    # 可以通过命令行参数传入song_id和comment_content
    # 用法1：python test_task_24.py                    # 自动检测最新评论
    # 用法2：python test_task_24.py song_002           # 手动指定歌曲ID
    # 用法3：python test_task_24.py song_002 "很棒"    # 手动指定歌曲ID和内容
    song_id = sys.argv[1] if len(sys.argv) > 1 else None
    comment_content = sys.argv[2] if len(sys.argv) > 2 else None
    success = test(song_id=song_id, comment_content=comment_content)

    print(f"任务24验证结果: {success}")
    sys.exit(0 if success else 1)