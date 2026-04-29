"""
指令 6 验证脚本：修改我的名字为123456

答案：123456

功能说明：
- 验证应用是否正确执行了修改用户名的任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：userName（用户名）、modified（是否已修改）

验证逻辑：
1. 使用 ADB 读取 6_modify_username.json 文件
2. 解析 JSON 内容
3. 验证 userName 字段包含 "123456"
4. 验证 modified 字段为 true（表示已完成修改）
5. 返回验证结果（PASS/FAIL）

步骤：3
"""

import json
import subprocess
import sys

# 预设的正确答案
EXPECTED_USERNAME = "123456"


def verify_modify_username(device_id=None):
    """
    验证修改用户名任务是否完成

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
            "files/6_modify_username.json"  # JSON 文件路径
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
        if "userName" not in json_data:
            print("❌ FAIL: 缺少 'userName' 字段")
            return False

        if "modified" not in json_data:
            print("❌ FAIL: 缺少 'modified' 字段")
            return False

        # 获取字段值
        user_name = json_data["userName"]
        modified = json_data["modified"]

        # 先显示当前状态，便于调试
        print(f"当前用户名: '{user_name}'")
        print(f"是否已修改: {modified}")
        print()

        # 验证是否已完成修改
        if not modified:
            print("❌ FAIL: 'modified' 字段为 false，任务未完成")
            print(f"   预期: modified = true")
            print(f"   实际: modified = {modified}")
            return False

        # 验证用户名是否完全匹配预设答案
        if str(user_name) != EXPECTED_USERNAME:
            print("❌ FAIL: 用户名不匹配预期答案")
            print(f"   预期答案: '{EXPECTED_USERNAME}'")
            print(f"   实际结果: '{user_name}'")
            if user_name == "":
                print(f"   提示: 用户名为空字符串")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 修改用户名任务验证成功")
        print(f"   用户名: {user_name}")
        print(f"   已修改: {modified}")

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
    print("指令 6 验证：修改我的名字为123456")
    print("=" * 60)

    # 执行验证
    success = verify_modify_username()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
