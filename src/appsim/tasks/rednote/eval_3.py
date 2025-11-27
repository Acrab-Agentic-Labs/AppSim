import json
import os
import subprocess


def search_and_view_check(result=None, device_id=None, backup_dir=None):
    """
    检查用户是否搜索了指定关键词并查看了指定数量的搜索结果
    任务3: 在搜索栏中输入"秋冬穿搭"，点击查看搜索结果页的前3条内容的详情
    """
    _USER_ID = "user_current"
    _SEARCH_QUERY = "秋冬穿搭"
    _VIEW_COUNT = 3

    message_file_path_1 = os.path.join(backup_dir, "search_history.json") if backup_dir is not None else "search_history.json"
    message_file_path_2 = os.path.join(backup_dir,"browsing_history.json") if backup_dir is not None else "browsing_history.json"

    try:
        # 从设备获取搜索历史文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/search_history.json"])
        with open(message_file_path_1, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path_1, "r", encoding="utf-8") as f:
            search_data = json.load(f)

        if not search_data or len(search_data) == 0:
            return False

        # 从设备获取浏览历史文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])

        with open(message_file_path_2, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path_2, "r", encoding="utf-8") as f:
            browsing_data = json.load(f)

        if not browsing_data or len(browsing_data) == 0:
            return False

        # 查找最新的搜索记录
        user_searches = [
            item for item in search_data if item.get("userId") == _USER_ID and item.get("query") == _SEARCH_QUERY
        ]

        if not user_searches:
            return False

        # 获取最新的搜索记录
        latest_search = sorted(user_searches, key=lambda x: x.get("searchedAt", ""), reverse=True)[0]
        search_time = latest_search.get("searchedAt")

        # 检查浏览记录中是否有从搜索结果进入的记录
        search_browsing = [
            item
            for item in browsing_data
            if item.get("userId") == _USER_ID
            and item.get("sourceType") == "SEARCH_RESULT"
            and item.get("browsedAt", "") >= search_time
        ]

        # 检查浏览数量是否达到预期
        if len(search_browsing) >= _VIEW_COUNT:
            return True
        else:
            return False

    except:
        return False


if __name__ == "__main__":
    print(search_and_view_check())
