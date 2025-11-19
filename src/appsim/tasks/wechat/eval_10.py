# 10、从“发现”进入我的朋友圈，依次浏览好友朋友圈，看看张杰最新一个朋友圈有多少人给他点赞了。告诉我数字即可。


def Task10_number_count(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    if "final_message" in result and (
        "15个" in result["final_message"]
        or "15人" in result["final_message"]
        or "十五个" in result["final_message"]
        or "十五个" in result["final_message"]
        or "15" in result["final_message"]
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = Task10_number_count()
    print(result)
