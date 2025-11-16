import subprocess
import json
import os
import shutil
import time


def CheckWatchHistory(result=None, device_id=None):
    """
    检验逻辑:查看观看历史
    验证用户是否在APP中真正查看了观看历史

    """
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.bilibili", "cat", "files/messages.json"])
    try:
        # step2. 读取logcat日志,查找特定的日志标记
        print("\n正在检查日志...")
        cmd_logcat = ["adb"]
        if device_id:
            cmd_logcat.extend(["-s", device_id])
        cmd_logcat.extend(["logcat", "-d", "-s", "BilibiliAutoTest:D"])

        result1 = subprocess.run(
            cmd_logcat,
            capture_output=True,
            encoding="utf-8",  # 强制使用utf-8编码（日志通常用utf-8）
            errors="replace",
            text=True,
            timeout=10,
        )

        log_content = result1.stdout

        # step3. 验证是否包含历史记录页面访问的日志
        if "HISTORY_TAB_VIEWED" not in log_content:
            print("❌ 验证失败: 未检测到进入历史记录页面")
            print("\n可能的原因:")
            print("1. 您没有点击进入历史记录页面")
            print("2. APP未正确安装或需要重新编译")
            print("\n日志内容:")
            print(log_content if log_content else "(无相关日志)")
            return False

        # step4. 验证是否成功加载了历史记录数据
        if "HISTORY_DATA_LOADED" not in log_content:
            print("❌ 验证失败: 历史记录数据未加载")
            print("\n日志内容:")
            print(log_content)
            return False

        # 提取加载的历史记录数量
        history_count = 0
        for line in log_content.split("\n"):
            if "HISTORY_DATA_LOADED" in line:
                try:
                    history_count = int(line.split(":")[-1].strip())
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
    except Exception as e:
        print(f"❌ 检查观看历史时发生错误: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    result1 = CheckWatchHistory()
    print(f"\n{'=' * 60}")
    print(f"最终检验结果: {'✓ 通过' if result1 else '✗ 失败'}")
    print(f"{'=' * 60}")
