def eval_35(result=None, device_id=None):
    """
    任务35: 数一下你喜欢的歌曲推荐数目
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
    # 检查是否包含数字（推荐数目）
    numbers = re.findall(r'\d+', final_msg)
    if numbers and any(keyword in final_msg for keyword in ["首", "歌", "曲", "数", "个", "推荐"]):
        print(f"  → AI返回了推荐数目信息: {final_msg}")
        return True
    else:
        print(f"  → AI返回的消息中未包含有效的推荐数目信息: {final_msg}")
        return False


if __name__ == "__main__":
    result = eval_35()
    print(result)
