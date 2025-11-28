import subprocess
import json
import os
import shutil
import time


def CheckOfflineCache(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:在我的页面，找到并点击"离线缓存"入口，进入离线缓存页面
    验证用户是否进入离线缓存页面
    """
    try:
        print("\n正在检查日志...")
        cmd_logcat = ['adb']
        if device_id:
            cmd_logcat.extend(['-s', device_id])
        cmd_logcat.extend(['logcat', '-d', '-s', 'BilibiliAutoTest:D'])

        result1 = subprocess.run(
            cmd_logcat,
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='ignore'
        )

        log_content = result1.stdout
        if backup_dir:
            logcat_file_path = os.path.join(backup_dir, 'logcat.txt')
            open(logcat_file_path, 'w', encoding='utf-8').write(log_content)

        # step3. 验证关键操作 - 只需要检测到进入离线缓存页面即可
        offline_cache_page_entered = 'OFFLINE_CACHE_PAGE_ENTERED' in log_content
        cache_list_loaded = 'CACHE_LIST_LOADED' in log_content

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
    finally:
        # 无论成功失败，最后都清除日志
        try:
            cmd_clear = ['adb']
            if device_id:
                cmd_clear.extend(['-s', device_id])
            cmd_clear.extend(['logcat', '-c'])
            subprocess.run(cmd_clear, timeout=5)
            print("🔄 已清除日志缓存")
        except subprocess.TimeoutExpired:
            print("⚠️ 清除日志超时")
        except Exception as e:
            print(f"⚠️ 清除日志失败: {str(e)}")

if __name__ == "__main__":
    result1 = CheckOfflineCache()
    print(result1)
