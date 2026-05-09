import re

# 4、看看我有多少个微信好友。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。

def task4_validate_friend_count(result=None, device_id=None, backup_dir=None):
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

        return match.group(1) == "101"
    except Exception:
        return False