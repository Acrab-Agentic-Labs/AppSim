# 3、查看北京大学李老师发给我的信息，看看参会的听众人数是多少，我好提前去订会议室。告诉我数字即可。


def Task3_number_count(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    if "final_message" in result and (
        "10人" in result["final_message"]
        or "10个" in result["final_message"]
        or "10位" in result["final_message"]
        or "十个" in result["final_message"]
        or "十个" in result["final_message"]
        or "十位" in result["final_message"]
        or "10" in result["final_message"]
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = Task3_number_count()
    print(result)
