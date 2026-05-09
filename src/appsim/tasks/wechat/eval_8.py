import re


# 8、看看12号到15号这几天，我的好友一共发了多少条朋友圈。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。


def task8_moments_count(result=None, device_id=None, backup_dir=None):
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

        return match.group(1) == "5"
    except Exception:
        return False


if __name__ == "__main__":
    result = task8_moments_count()
    print(result)
