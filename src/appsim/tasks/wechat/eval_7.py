# 7、从“发现”进入我的朋友圈，看前五条好友朋友圈，告诉我，我已经点赞了多少条。告诉我数字即可。


def Task7_number_count(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    if "final_message" in result and (
        "4个" in result["final_message"]
        or "4条" in result["final_message"]
        or "四个" in result["final_message"]
        or "四条" in result["final_message"]
        or "4" in result["final_message"]
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = Task7_number_count()
    print(result)
