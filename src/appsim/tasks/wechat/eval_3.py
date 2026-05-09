import re


# 3、查看北京大学李老师发给我的信息，看看参会的听众人数是多少，我好提前去订会议室。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。


def task3_validate_attendee_count(result=None, device_id=None, backup_dir=None):
    try:
        if not isinstance(result, dict):
            return False

        final_msg = result.get("final_message")
        if final_msg is None:
            return False

        final_msg = str(final_msg)
        match = re.search(
            r"<ans>\s*(\d+)\s*</ans>",
            final_msg,
            re.IGNORECASE | re.DOTALL,
        )
        if match is None:
            return False

        return match.group(1) == "10"
    except Exception:
        return False


if __name__ == "__main__":
    result = task3_validate_attendee_count()
    print(result)
