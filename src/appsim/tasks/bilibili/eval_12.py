import subprocess


def CheckOfflineCache(result=None, device_id=None):
    """
    检验逻辑:在我的页面，找到并点击"离线缓存"入口，进入离线缓存页面
    验证用户是否进入离线缓存页面
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])

        print("=" * 60)
        print("请在虚拟机中执行以下操作:")
        print("1. 打开bilibili APP")
        print("2. 点击底部'我的'页面")
        print("3. 找到并点击'离线缓存'入口")
        print("4. 进入离线缓存页面")
        print("=" * 60)

        # step2. 读取logcat日志
        print("\n正在检查日志...")
        cmd_logcat = ["adb"]
        if device_id:
            cmd_logcat.extend(["-s", device_id])
        cmd_logcat.extend(["logcat", "-d", "-s", "BilibiliAutoTest:D"])

        result1 = subprocess.run(
            cmd_logcat,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="ignore",  # 忽略无法解码的字符
        )

        log_content = result1.stdout

        # step3. 验证关键操作 - 只需要检测到进入离线缓存页面即可
        offline_cache_page_entered = "OFFLINE_CACHE_PAGE_ENTERED" in log_content
        cache_list_loaded = "CACHE_LIST_LOADED" in log_content

        if not (offline_cache_page_entered or cache_list_loaded):
            print("验证失败: 未检测到进入离线缓存页面")
            print("\n提示: 请确保:")
            print("1. 在我的页面点击了'离线缓存'")
            print("2. 已进入离线缓存页面")
            return False

        print("离线缓存页面验证成功!")
        return True

    except subprocess.TimeoutExpired:
        print("验证失败: 读取日志超时")
        return False
    except Exception as e:
        print(f"检查离线缓存页面时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    result1 = CheckOfflineCache()
    print(result1)
