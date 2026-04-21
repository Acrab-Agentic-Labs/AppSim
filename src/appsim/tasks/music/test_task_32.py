"""
任务32：数一下歌曲《晴天》的评论数目
难度：中
类型：信息检索/推理类
"""

import logging
import sys
import re
from .verification_functions import read_json_from_device

SONG_NAME_FOR_TASK = "晴天"

def find_song_id_by_name(song_name, device_id, result, backup_dir):
    """辅助函数：根据歌曲名称查找ID"""
    songs_data = read_json_from_device("autotest/playlists.json", device_id, result, backup_dir)
    if not songs_data or "songs" not in songs_data or not isinstance(songs_data.get("songs"), list):
        logging.error("  → 错误：无法读取歌曲列表 'autotest/playlists.json'")
        return None
    
    for song in songs_data["songs"]:
        if song.get("songName") == song_name:
            return song.get("songId")
            
    logging.error(f"  → 错误：在 'autotest/playlists.json' 中未找到名为 '{song_name}' 的歌曲")
    return None

def check_comment_count(result=None, device_id=None, backup_dir=None):
    """
    任务32: 核实《晴天》的评论数
    - 动态查找《晴天》的ID
    - 从AI回答中解析出评论数
    - 从设备读取comments.json计算实际评论数
    - 对比两者是否一致
    """
    if not result or "final_message" not in result:
        logging.error("✗ 测试失败 - 任务32未完成：AI未提供final_message")
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        logging.error(f"✗ 测试失败 - 任务32未完成：final_message格式错误: {final_msg}")
        return False

    # 1. 动态查找歌曲ID
    song_id = find_song_id_by_name(SONG_NAME_FOR_TASK, device_id, result, backup_dir)
    if not song_id:
        logging.error(f"✗ 测试失败 - 任务32未完成：无法动态获取歌曲 '{SONG_NAME_FOR_TASK}' 的ID")
        return False
    logging.info(f"  → 动态查找到歌曲 '{SONG_NAME_FOR_TASK}' 的ID为: {song_id}")

    # 2. 从AI回答中解析出数字
    numbers = re.findall(r'\d+', final_msg)
    if not numbers:
        logging.error(f"✗ 测试失败 - 任务32未完成：未能在AI的回答中找到任何数字: '{final_msg}'")
        return False
    agent_count = int(numbers[0])
    logging.info(f"  → AI报告的评论数为: {agent_count}")

    # 3. 从设备读取真实评论数据
    comments_data = read_json_from_device("autotest/comments.json", device_id, result, backup_dir)
    if not comments_data or "allComments" not in comments_data or not isinstance(comments_data.get("allComments"), dict):
        logging.error("✗ 测试失败 - 任务32未完成：无法从设备读取评论数据或'allComments'字段格式不正确")
        return False

    # 4. 计算真实值
    device_count = 0
    if song_id in comments_data["allComments"]:
        device_count = len(comments_data["allComments"][song_id])
    logging.info(f"  → 设备中歌曲ID '{song_id}' 的实际评论数为: {device_count}")

    # 5. 对比验证
    if agent_count == device_count:
        logging.info("✓ 测试通过 - 任务32完成：AI报告的评论数与设备实际评论数一致")
        return True
    else:
        logging.error(f"✗ 测试失败 - 任务32未完成：AI报告的评论数({agent_count})与设备实际评论数({device_count})不符")
        return False

if __name__ == "__main__":

    print(check_comment_count())
