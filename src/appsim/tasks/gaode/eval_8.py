"""
指令 8 验证脚本：打开夜间模式

答案：夜间模式 或 夜间 或 dark

功能说明：
- 验证应用是否正确执行了打开夜间模式的任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：mode（模式）、opened（是否已打开）

验证逻辑：
1. 使用 ADB 读取 8_open_bright_mode.json 文件
2. 解析 JSON 内容
3. 验证 mode 字段包含 "夜间" 或 "dark"
4. 验证 opened 字段为 true（表示已打开）
5. 返回验证结果（PASS/FAIL）

步骤：2
"""

import json
import subprocess
import sys

# 预设的正确答案（可能的表达方式）
EXPECTED_MODES = ["夜间", "dark", "夜间模式"]


def verify_open_bright_mode(device_id=None):
    """
    验证打开夜间模式任务是否完成

    参数：
        device_id (str): Android 设备 ID，如果为 None 则使用默认设备

    返回：
        bool: 验证通过返回 True，否则返回 False
    """
    try:
        # 构建 ADB 命令，读取应用私有存储中的 JSON 文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend([
            "exec-out",
            "run-as",
            "com.example.amap_sim",  # 应用包名
            "cat",
            "files/8_open_bright_mode.json"  # JSON 文件路径
        ])

        print("正在执行 ADB 命令读取文件...")
        result = subprocess.run(cmd, capture_output=True, text=False, check=True)

        # 处理输出编码（支持 UTF-8 和 GBK）
        try:
            stdout_text = result.stdout.decode("utf-8")
        except UnicodeDecodeError:
            try:
                stdout_text = result.stdout.decode("gbk")
            except UnicodeDecodeError:
                stdout_text = result.stdout.decode("utf-8", errors="ignore")

        # 检查文件是否为空
        if not stdout_text.strip():
            print("❌ FAIL: JSON 文件为空")
            return False

        # 解析 JSON 内容
        print("正在解析 JSON 内容...")
        json_data = json.loads(stdout_text)

        # 验证必要字段是否存在
        if "mode" not in json_data:
            print("❌ FAIL: 缺少 'mode' 字段")
            return False

        if "opened" not in json_data:
            print("❌ FAIL: 缺少 'opened' 字段")
            return False

        # 获取字段值
        mode = json_data["mode"]
        opened = json_data["opened"]

        # 验证模式是否包含预设答案中的任意一个
        found_match = False
        matched_mode = None
        for expected in EXPECTED_MODES:
            if expected in str(mode).lower():
                found_match = True
                matched_mode = expected
                break

        if not found_match:
            print("❌ FAIL: 模式中未包含预期答案")
            print(f"   预期答案（任意一个）: {', '.join(EXPECTED_MODES)}")
            print(f"   实际结果: {mode}")
            return False

        # 验证是否已打开
        if not opened:
            print("❌ FAIL: 'opened' 字段为 false，任务未完成")
            print(f"   当前值: {opened}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 打开夜间模式任务验证成功")
        print(f"   模式: {mode}")
        print(f"   匹配到的答案: {matched_mode}")
        print(f"   已打开: {opened}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ FAIL: ADB 命令执行失败 - {e}")
        try:
            error_text = e.stderr.decode("utf-8") if e.stderr else "无错误输出"
        except:
            error_text = "无法解码错误信息"
        print(f"   错误信息: {error_text}")
        return False

    except json.JSONDecodeError as e:
        print(f"❌ FAIL: JSON 解析错误 - {e}")
        print(f"   原始内容: {stdout_text}")
        return False

    except Exception as e:
        print(f"❌ FAIL: 未预期的错误 - {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("指令 8 验证：打开夜间模式")
    print("=" * 60)

    # 执行验证
    success = verify_open_bright_mode()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
