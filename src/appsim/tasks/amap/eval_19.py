"""
指令 19 验证脚本：拨打周边景点排行榜第一的景点电话

答案：庚子革命烈士墓墓道牌坊

功能说明：
- 验证应用是否正确执行了拨打景点电话的任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：name（景点名称）、phone（电话）、called（是否已拨打）

验证逻辑：
1. 使用 ADB 读取 19_call_top_attraction.json 文件
2. 解析 JSON 内容
3. 验证 name 字段包含 "庚子革命烈士墓墓道牌坊"
4. 验证 phone 字段不为空
5. 验证 called 字段为 true（表示已拨打电话）
6. 返回验证结果（PASS/FAIL）

步骤：6
"""

import json
import subprocess
import sys

# 预设的正确答案
EXPECTED_NAME = "庚子革命烈士墓墓道牌坊"


def verify_call_top_attraction(device_id=None):
    """
    验证拨打景点电话任务是否完成

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
            "files/19_call_top_attraction.json"  # JSON 文件路径
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
        if "name" not in json_data:
            print("❌ FAIL: 缺少 'name' 字段")
            return False

        if "phone" not in json_data:
            print("❌ FAIL: 缺少 'phone' 字段")
            return False

        if "called" not in json_data:
            print("❌ FAIL: 缺少 'called' 字段")
            return False

        # 获取字段值
        name = json_data["name"]
        phone = json_data["phone"]
        called = json_data["called"]

        # 验证景点名称是否包含预设答案
        if EXPECTED_NAME not in str(name):
            print("❌ FAIL: 景点名称中未包含预期答案")
            print(f"   预期答案: {EXPECTED_NAME}")
            print(f"   实际结果: {name}")
            return False

        # 验证电话号码是否有效
        if not phone or phone == "":
            print("❌ FAIL: 'phone' 字段为空")
            print(f"   当前值: '{phone}'")
            return False

        # 验证是否已拨打电话
        if not called:
            print("❌ FAIL: 'called' 字段为 false，任务未完成")
            print(f"   当前值: {called}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 拨打景点电话任务验证成功")
        print(f"   景点名称: {name}")
        print(f"   电话号码: {phone}")
        print(f"   已拨打: {called}")

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
    print("指令 19 验证：拨打周边景点排行榜第一的景点电话")
    print("=" * 60)

    # 执行验证
    success = verify_call_top_attraction()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
