import json
import subprocess


def BrowsingHistoryCheck(result=None, device_id=None):
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])
    # 从设备获取文件
    result1 = subprocess.run(cmd, stdout=open("browsing_history.json", "w"))
    if result1.returncode != 0 or not result1.stdout:
        return False
    # 读取文件
    with open("browsing_history.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 检查最后一条浏览历史数据
    try:
        # 获取最后一条数据
        last_item = data[-1]

        # 检查 noteAuthor.id 和 noteTitle
        if (
            last_item.get("noteAuthor", {}).get("id") == "user_002"
            and last_item.get("noteTitle") == "秋冬穿搭指南 | 温暖又时尚的搭配技巧"
        ):
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    print(BrowsingHistoryCheck())
