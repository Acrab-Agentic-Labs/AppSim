# 12、查看工作讨论组的消息，是谁完成了设计稿？告诉我答案即可。


def task12_validate_design_draft_person(result=None, device_id=None, backup_dir=None):
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    if "周浩然" in final_msg:
        return True
    else:
        return False


if __name__ == "__main__":
    result = task12_validate_design_draft_person()
    print(result)
