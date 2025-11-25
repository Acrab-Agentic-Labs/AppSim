def eval_32(result=None, device_id=None, backup_dir=None):
    """
    任务32: 数一下歌曲晴天的评论的数目
    验证: 检查final_message中是否包含数字信息
    """
    if result is None:
        return False

    if "final_message" not in result:
        return False

    final_msg = result["final_message"]
    if not final_msg or not isinstance(final_msg, str):
        return False

    import re
    # 检查是否包含数字（评论数目）
    numbers = re.findall(r'\d+', final_msg)
    if numbers and any(keyword in final_msg for keyword in ["评论", "条", "个", "数"]):
        print(f"  → AI返回了评论数目信息: {final_msg}")
        return True
    else:
        print(f"  → AI返回的消息中未包含有效的评论数目信息: {final_msg}")
        return False


if __name__ == "__main__":
    result = eval_32()
    print(result)
