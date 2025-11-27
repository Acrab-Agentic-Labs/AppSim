import subprocess
import json
import os
import shutil
import time


def CheckSearchGame1(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:在首页搜索框输入游戏解说，点击搜索按钮
    验证用户是否完成搜索操作
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

        # step3. 验证是否输入了搜索内容
        if 'SEARCH_INPUT' not in log_content or '游戏解说' not in log_content:
            print("验证失败: 未检测到输入'游戏解说'")
            print(f"日志内容:\n{log_content}")
            return False

        # step4. 验证是否点击了搜索按钮
        if 'SEARCH_BUTTON_CLICKED' not in log_content:
            print("验证失败: 未检测到点击搜索按钮")
            print(f"日志内容:\n{log_content}")
            return False

        # step5. 验证是否成功跳转到游戏搜索结果页面
        if 'GAME_SEARCH_PAGE_LOADED' not in log_content:
            print("验证失败: 未成功跳转到游戏搜索结果页面")
            print(f"日志内容:\n{log_content}")
            return False


        # 验证 result 存在
        if result is None:
            return False

        # 检测 result 中的final_messages中是否包含数字"3"（作为独立的数字）
        # 使用正则表达式精确匹配，避免匹配到"30"、"13"、"300"等包含3的数字
        if 'final_message' in result:
            # 匹配独立的数字3，可以是"3个"、"3 个"、"共3个"等形式
            pattern = r'(?:^|[^\d])3(?:[^\d]|$)'
            if re.search(pattern, result['final_message']):
                return True

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
    result1 = CheckSearchGame1()
    print(result1)
