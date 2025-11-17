import json
import subprocess


def SearchAndViewCheck(userId="user_current", searchQuery="秋冬穿搭", viewCount=3, result=None, device_id=None):
    """
    检查用户是否搜索了指定关键词并查看了指定数量的搜索结果
    任务3: 在搜索栏中输入"秋冬穿搭"，点击查看搜索结果页的前3条内容的详情
    """
    # 从设备获取搜索历史文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/search_history.json"])

    search_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 从设备获取浏览历史文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"])

    browsing_result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if search_result.returncode != 0 or not search_result.stdout:
        # print(f"❌ Failed to read search history file")
        # print(f"   Reason: ADB command failed (return code: {search_result.returncode})")
        # if search_result.stderr:
        # print(f"   Error: {search_result.stderr}")
        return False
    if browsing_result.returncode != 0 or not browsing_result.stdout:
        # print(f"❌ Failed to read browsing history file")
        # print(f"   Reason: ADB command failed (return code: {browsing_result.returncode})")
        # if browsing_result.stderr:
        # print(f"   Error: {browsing_result.stderr}")
        return False

    # 解析 JSON
    try:
        search_data = json.loads(search_result.stdout)
        browsing_data = json.loads(browsing_result.stdout)
    except:
        # print(f"❌ Failed to parse JSON data")
        # print(f"   Reason: Invalid JSON format")
        return False

    # 检查搜索历史和浏览记录
    try:
        # 检查是否有搜索记录
        if not search_data or len(search_data) == 0:
            # print(f"❌ Search history is empty")
            # print(f"   Reason: No search records found")
            # print(f"   Expected: Search query '{searchQuery}'")
            return False

        # 查找最新的搜索记录
        user_searches = [
            item for item in search_data if item.get("userId") == userId and item.get("query") == searchQuery
        ]

        if not user_searches:
            # print(f"❌ Search query not found")
            # print(f"   Reason: User '{userId}' did not search for '{searchQuery}'")
            # Show recent searches
            recent_searches = [item.get("query", "UNKNOWN") for item in search_data if item.get("userId") == userId][:5]
            # if recent_searches:
            # print(f"   Recent searches: {recent_searches}")
            return False

        # 获取最新的搜索记录
        latest_search = sorted(user_searches, key=lambda x: x.get("searchedAt", ""), reverse=True)[0]
        search_time = latest_search.get("searchedAt")

        # 检查浏览记录中是否有从搜索结果进入的记录
        search_browsing = [
            item
            for item in browsing_data
            if item.get("userId") == userId
            and item.get("sourceType") == "SEARCH_RESULT"
            and item.get("browsedAt", "") >= search_time
        ]

        # 检查浏览数量是否达到预期
        if len(search_browsing) >= viewCount:
            # print(f"✓ Successfully searched '{searchQuery}' and viewed {viewCount} results")
            return True
        else:
            # print(f"❌ Not enough search result views")
            # print(f"   Reason: Found {len(search_browsing)} views, expected {viewCount}")
            # print(f"   Search query: '{searchQuery}' at {search_time}")
            return False

    except:
        # print(f"❌ Error while checking search and browsing data")
        return False


if __name__ == "__main__":
    print(SearchAndViewCheck(userId="user_current", searchQuery="秋冬穿搭", viewCount=3))
