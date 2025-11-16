# 8、看看12号到15号这几天，我的好友一共发了多少条朋友圈。告诉我数字即可。


def Task8_number_count(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    if "final_message" in result and (
        "5个" in result["final_message"]
        or "5条" in result["final_message"]
        or "五个" in result["final_message"]
        or "五条" in result["final_message"]
        or "5" in result["final_message"]
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = Task8_number_count()
    print(result)
