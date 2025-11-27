# 9、好友张杰的新歌名字叫什么来着，有点忘记了，你翻一下我和他的聊天记录。告诉我答案即可。


def task9_song_name_check(result=None, device_id=None, backup_dir=None) -> bool:
    # 验证 result 存在
    if result is None:
        return False

    # 安全获取 final_message，如果为 None 则默认为空字符串
    final_msg = result.get("final_message") or ""

    return "秋日私语" in final_msg


if __name__ == "__main__":
    result = task9_song_name_check()
    print(result)
