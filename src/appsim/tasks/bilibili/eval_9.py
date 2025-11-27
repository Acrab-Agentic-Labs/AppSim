import subprocess
import json
import os
import shutil
import time



def CheckProfilePage(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:在我的页面，点击顶部头像或昵称区域，进入个人资料页查看信息
    验证用户是否进入个人资料页
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

        # step3. 验证关键操作 - 只需要检测到PersonTab即可
        person_tab_detected = 'PersonTab' in log_content

        if not person_tab_detected:
            print("验证失败: 未检测到PersonTab")
            print("\n提示: 请确保:")
            print("1. 在我的页面点击了顶部头像或昵称")
            print("2. 已进入个人资料页")
            print(f"\n日志内容:\n{log_content}")
            return False

        # 验证 result 存在
        if result is None:
            return False

        # 检测 result 中的final_messages中是否包含 "凡人修仙传"
        if 'final_message' in result and '凡人修仙传' in result['final_message']:
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
    result1 = CheckProfilePage()
    print(result1)
