# 7、从“发现”进入我的朋友圈，看前五条好友朋友圈，告诉我，我已经点赞了多少条。告诉我数字即可。


def task7_stared_moments_count(result=None, device_id=None, backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    if (
        "四个" in final_msg
        or "四条" in final_msg
        or "4" in final_msg
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = task7_stared_moments_count()
    print(result)
