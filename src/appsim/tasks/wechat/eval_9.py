# 9、好友张杰的新歌名字叫什么来着，有点忘记了，你翻一下我和他的聊天记录。告诉我答案即可。


def Task9_song_find(result=None, device_id=None) -> bool:
    # 验证 result 存在
    if result is None:
        return False

    return bool("final_message" in result and "秋日私语" in result["final_message"])


if __name__ == "__main__":
    result = Task9_song_find()
    print(result)
