# 3、查看北京大学李老师发给我的信息，看看参会的听众人数是多少，我好提前去订会议室。告诉我数字即可。


def task3_validate_attendee_count(result=None, device_id=None, backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    if (
        "十个" in final_msg
        or "十人" in final_msg
        or "十位" in final_msg
        or "10" in final_msg
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = task3_validate_attendee_count()
    print(result)
