import re


# 9、好友张杰的新歌名字叫什么来着，有点忘记了，你翻一下我和他的聊天记录。把你的答案放置在<ans>和</ans>之间，你的答案必须是歌曲名。


def task9_song_name_check(result=None, device_id=None, backup_dir=None) -> bool:
    try:
        if not isinstance(result, dict):
            return False

        final_msg = result.get("final_message")
        if final_msg is None:
            return False

        final_msg = str(final_msg)
        match = re.search(
            r"<ans>\s*(.*?)\s*</ans>",
            final_msg,
            re.IGNORECASE | re.DOTALL,
        )
        if match is None:
            return False

        return match.group(1).strip() == "秋日私语"
    except Exception:
        return False


if __name__ == "__main__":
    result = task9_song_name_check()
    print(result)
