import subprocess
import json
import os
import shutil
import time



def CheckWatchHistory(result=None,device_id=None,backup_dir=None):
    """
    检验逻辑:查看观看历史
    验证用户是否在APP中真正查看了观看历史

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
            encoding='utf-8',
            errors='replace',
            text=True,
            timeout=10
        )

        log_content = result1.stdout
        if backup_dir:
            logcat_file_path = os.path.join(backup_dir, 'logcat.txt')
            open(logcat_file_path, 'w', encoding='utf-8').write(log_content)

        # step3. 验证是否包含历史记录页面访问的日志
        if 'HISTORY_TAB_VIEWED' not in log_content:
            print("❌ 验证失败: 未检测到进入历史记录页面")
            print("\n可能的原因:")
            print("1. 您没有点击进入历史记录页面")
            print("2. APP未正确安装或需要重新编译")
            print("\n日志内容:")
            print(log_content if log_content else "(无相关日志)")
            return False

        # step4. 验证是否成功加载了历史记录数据
        if 'HISTORY_DATA_LOADED' not in log_content:
            print("❌ 验证失败: 历史记录数据未加载")
            print("\n日志内容:")
            print(log_content)
            return False

        # 提取加载的历史记录数量
        history_count = 0
        
        for line in log_content.split('\n'):
            if 'HISTORY_DATA_LOADED' in line:
                try:
                    history_count = int(line.split(':')[-1].strip())
                except:
                    pass

        print("✓ 检测到进入历史记录页面")
        print(f"✓ 成功加载历史记录数据 (共{history_count}条)")
        print("\n" + "=" * 60)
        print("观看历史验证成功!")
        print("=" * 60)
        return True

    except subprocess.TimeoutExpired:
        print("❌ 验证失败: 读取日志超时")
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
    result1 = CheckWatchHistory()
    print(f"\n{'='*60}")
    print(f"最终检验结果: {'✓ 通过' if result1 else '✗ 失败'}")
    print(f"{'='*60}")
