# 5、看看家庭群，确定一下周六几点集合？在哪集合？告诉我答案即可。


def task5_validate_info_in_group(result=None, device_id=None, backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    if ("9点" in final_msg or "九点" in final_msg) and "香山门口" in final_msg:
        return True
    else:
        return False


if __name__ == "__main__":
    result = task5_validate_info_in_group()
    print(result)
