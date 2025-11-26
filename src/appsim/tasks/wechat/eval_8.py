# 8、看看12号到15号这几天，我的好友一共发了多少条朋友圈。告诉我数字即可。


def task8_moments_count(result=None, device_id=None, backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    if (
        "五个" in final_msg
        or "五条" in final_msg
        or "5" in final_msg
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = task8_moments_count()
    print(result)
