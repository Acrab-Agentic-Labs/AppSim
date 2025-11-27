# 4、看看我有多少个微信好友。告诉我数字即可。


def task4_validate_friend_count(result=None, device_id=None, backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    if "21" in final_msg or "二十一" in final_msg:
        return True
    else:
        return False


if __name__ == "__main__":
    result = task4_validate_friend_count()
    print(result)
