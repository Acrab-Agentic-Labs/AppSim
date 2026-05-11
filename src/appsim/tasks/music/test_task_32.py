"""
任务32：告诉我"晴天"的第一条评论的发布时间
难度：中
类型：信息检索/推理类
"""

import logging
import re
from datetime import datetime
from .verification_functions import read_json_from_device

SONG_NAME_FOR_TASK = "晴天"


def check_first_comment_time_reported(result=None, device_id=None, backup_dir=None):
    """
    任务32: 验证AI是否正确报告了"晴天"第一条评论的发布时间
    - 从设备读取comments.json，找到晴天的第一条评论
    - 提取其时间戳并转换为可读格式
    - 检查AI的final_message是否包含正确的时间信息
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务32未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务32未完成：final_message格式错误: {final_msg}")
        return False

    # 从设备读取评论数据
    comments_data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments_data:
        logging.error("✗ 测试失败 - 任务32未完成：无法读取评论数据")
        return False

    # 查找晴天的评论
    song_comments = None
    all_comments = comments_data.get("allComments", {})
    if isinstance(all_comments, dict):
        # 尝试通过歌曲ID查找
        for song_id, comments in all_comments.items():
            if isinstance(comments, list) and len(comments) > 0:
                if any(SONG_NAME_FOR_TASK in str(c) for c in comments):
                    song_comments = comments
                    break
        # 直接用song_001查找
        if not song_comments and "song_001" in all_comments:
            song_comments = all_comments["song_001"]
    elif isinstance(all_comments, list):
        song_comments = all_comments

    if not song_comments or len(song_comments) == 0:
        logging.error("✗ 测试失败 - 任务32未完成：未找到晴天的评论数据")
        return False

    # 获取第一条评论的时间戳
    first_comment = song_comments[0]
    timestamp = first_comment.get("timestamp", 0)
    if not timestamp:
        logging.error("✗ 测试失败 - 任务32未完成：第一条评论没有时间戳")
        return False

    # 转换时间戳为多种可能的格式进行匹配
    try:
        if timestamp > 1e12:
            dt = datetime.fromtimestamp(timestamp / 1000)
        else:
            dt = datetime.fromtimestamp(timestamp)

        # 生成多种可能的时间格式
        possible_formats = [
            dt.strftime("%Y-%m-%d"),
            dt.strftime("%Y年%m月%d日"),
            dt.strftime("%Y/%m/%d"),
            dt.strftime("%m月%d日"),
            dt.strftime("%Y.%m.%d"),
            str(dt.year),
        ]
        logging.info(f"  → 第一条评论时间戳: {timestamp}, 转换为: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    except (ValueError, OSError):
        logging.error(f"✗ 测试失败 - 任务32未完成：时间戳转换失败: {timestamp}")
        return False

    # 检查AI回答是否包含时间信息
    for fmt in possible_formats:
        if fmt in final_msg:
            logging.info(f"✓ 测试通过 - 任务32完成：AI正确报告了评论发布时间（匹配格式: {fmt}）")
            return True

    # 也检查数字匹配（年月日）
    year_str = str(dt.year)
    month_str = str(dt.month)
    day_str = str(dt.day)
    if year_str in final_msg and month_str in final_msg and day_str in final_msg:
        logging.info(f"✓ 测试通过 - 任务32完成：AI正确报告了评论发布时间（包含年月日数字）")
        return True

    logging.error(f"✗ 测试失败 - 任务32未完成：AI的回答'{final_msg}'中未包含正确的时间信息。期望包含: {possible_formats}")
    return False


if __name__ == "__main__":
    print(check_first_comment_time_reported())
