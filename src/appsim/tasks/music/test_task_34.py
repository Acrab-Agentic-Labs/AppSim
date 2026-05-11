"""
任务34：告诉我"七里香"的第三条评论是什么
难度：中
类型：信息检索/推理类
"""

import logging
from .verification_functions import read_json_from_device

SONG_NAME_FOR_TASK = "七里香"


def check_third_comment_content_reported(result=None, device_id=None, backup_dir=None):
    """
    任务34: 验证AI是否正确报告了"七里香"第三条评论的内容
    - 从设备读取comments.json，找到七里香的第三条评论
    - 检查AI的final_message是否包含该评论内容
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务34未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务34未完成：final_message格式错误: {final_msg}")
        return False

    # 从设备读取评论数据
    comments_data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments_data:
        logging.error("✗ 测试失败 - 任务34未完成：无法读取评论数据")
        return False

    # 查找七里香的评论
    song_comments = None
    all_comments = comments_data.get("allComments", {})
    if isinstance(all_comments, dict):
        # 尝试通过song_003查找
        if "song_003" in all_comments:
            song_comments = all_comments["song_003"]
        else:
            for song_id, comments in all_comments.items():
                if isinstance(comments, list) and len(comments) > 0:
                    if any(SONG_NAME_FOR_TASK in str(c) for c in comments):
                        song_comments = comments
                        break

    if not song_comments or len(song_comments) < 3:
        logging.error(f"✗ 测试失败 - 任务34未完成：七里香的评论数据不足3条，实际: {len(song_comments) if song_comments else 0}")
        return False

    # 获取第三条评论的内容
    third_comment = song_comments[2]
    comment_content = third_comment.get("content", "")
    if not comment_content:
        logging.error("✗ 测试失败 - 任务34未完成：第三条评论内容为空")
        return False

    logging.info(f"  → 七里香第三条评论内容: '{comment_content}'")

    # 检查AI回答是否包含评论内容
    if comment_content in final_msg:
        logging.info("✓ 测试通过 - 任务34完成：AI正确报告了第三条评论内容")
        return True
    else:
        # 尝试部分匹配（评论内容的前半部分）
        half_content = comment_content[:len(comment_content)//2]
        if half_content and half_content in final_msg:
            logging.info("✓ 测试通过 - 任务34完成：AI报告了第三条评论的部分内容")
            return True
        logging.error(f"✗ 测试失败 - 任务34未完成：AI的回答'{final_msg}'中未包含第三条评论内容'{comment_content}'")
        return False


if __name__ == "__main__":
    print(check_third_comment_content_reported())
