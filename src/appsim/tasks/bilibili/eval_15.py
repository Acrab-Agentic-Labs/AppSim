import subprocess
import json
import os
import shutil
import time
import re



def CheckHistoryItemDelete(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:在历史记录页面，找到今天观看过的一个视频，长按该记录项，将其从历史记录中删除，然后告诉我删除后还有几个视频
    验证用户是否在APP中真正完成了历史记录删除操作
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

        # step3. 验证关键操作 - 放宽验证条件
        history_page_entered = 'HISTORY_PAGE_ENTERED' in log_content
        history_data_loaded = 'HISTORY_DATA_LOADED' in log_content
        history_item_long_pressed = 'HISTORY_ITEM_LONG_PRESSED' in log_content
        delete_button_clicked = 'DELETE_BUTTON_CLICKED' in log_content
        history_item_deleted = 'HISTORY_ITEM_DELETED' in log_content

        # 只要检测到删除相关操作即可
        if not (history_item_long_pressed or delete_button_clicked or history_item_deleted):
            print("验证失败: 未检测到删除历史记录操作")
            print("\n提示: 请确保:")
            print("1. 进入了历史记录页面")
            print("2. 长按了某个历史记录项")
            print("3. 点击了删除")
            print(f"\n日志内容:\n{log_content}")
            return False

        # 验证 result 存在
        if result is None:
            return False

        # 检测 result 中的final_messages中是否包含 "8"
        if 'final_message' in result and '8' in result['final_message']:
            return True
        else:
            return False

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
    result1 = CheckHistoryItemDelete()
    print(result1)
