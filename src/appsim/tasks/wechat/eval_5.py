# 5、看看家庭群，确定一下周六几点集合？在哪集合？告诉我答案即可。


def Task5_info_search(result=None, device_id=None):
    # 验证 result 存在
    if result is None:
        return False

    if "final_message" in result and (
        ("9点" in result["final_message"] or "九点" in result["final_message"])
        and "香山门口" in result["final_message"]
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = Task5_info_search()
    print(result)
