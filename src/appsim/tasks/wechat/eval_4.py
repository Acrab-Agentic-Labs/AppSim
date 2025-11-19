# 4、看看我有多少个微信好友。告诉我数字即可。


def Task4_number_count(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    if "final_message" in result and ("21" in result["final_message"] or "二十一" in result["final_message"]):
        return True
    else:
        return False


if __name__ == "__main__":
    result = Task4_number_count()
    print(result)
