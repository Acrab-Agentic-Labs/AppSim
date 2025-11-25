# 10、从“发现”进入我的朋友圈，依次浏览好友朋友圈，看看张杰最新一个朋友圈有多少人给他点赞了。告诉我数字即可。


def task10_validate_latest_friend_like_count(result=None, device_id=None, backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    if (
        "15个" in final_msg
        or "15人" in final_msg
        or "十五个" in final_msg
        or "十五个" in final_msg
        or "15" in final_msg
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = task10_validate_latest_friend_like_count()
    print(result)
