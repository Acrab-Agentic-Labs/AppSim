import re


# 10、从“发现”进入我的朋友圈，依次浏览好友朋友圈，看看张杰最新一个朋友圈有多少人给他点赞了。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。


def task10_validate_latest_friend_like_count(result=None, device_id=None, backup_dir=None):
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

        return match.group(1) == "14"
    except Exception:
        return False


if __name__ == "__main__":
    result = task10_validate_latest_friend_like_count()
    print(result)
