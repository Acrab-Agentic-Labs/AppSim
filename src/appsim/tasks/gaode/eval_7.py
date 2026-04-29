"""
指令 7 验证脚本：步行导航去M+购物中心

答案：M+购物中心 或 M+，并且是步行导航

功能说明：
- 验证应用是否正确执行了步行导航任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：destination（目的地）、started（是否已开始导航）

验证逻辑：
1. 使用 ADB 读取 7_navigate_to_destination.json 文件
2. 解析 JSON 内容
3. 验证 destination 字段包含 "M+" 或 "M+购物中心"
4. 验证 destination 字段包含 "步行" 关键词
5. 验证 started 字段为 true（表示已开始导航）
6. 返回验证结果（PASS/FAIL）

步骤：最少5
"""

import json
import subprocess
import sys

# 预设的正确答案（可能的表达方式）
EXPECTED_DESTINATIONS = ["M+", "M+购物中心"]


def verify_navigate_to_destination(device_id=None):
    """
    验证导航任务是否完成

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
            "files/7_navigate_to_destination.json"  # JSON 文件路径
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
        if "destination" not in json_data:
            print("❌ FAIL: 缺少 'destination' 字段")
            return False

        if "started" not in json_data:
            print("❌ FAIL: 缺少 'started' 字段")
            return False

        # 获取字段值
        destination = json_data["destination"]
        started = json_data["started"]

        # 验证目的地是否包含预设答案中的任意一个
        found_match = False
        matched_destination = None
        for expected in EXPECTED_DESTINATIONS:
            if expected in str(destination):
                found_match = True
                matched_destination = expected
                break

        if not found_match:
            print("❌ FAIL: 目的地中未包含预期答案")
            print(f"   预期答案（任意一个）: {', '.join(EXPECTED_DESTINATIONS)}")
            print(f"   实际结果: {destination}")
            return False

        # 验证是否包含"步行"关键词
        if "步行" not in str(destination):
            print("❌ FAIL: 目的地中未包含'步行'关键词")
            print(f"   实际结果: {destination}")
            return False

        # 验证是否已开始导航
        if not started:
            print("❌ FAIL: 'started' 字段为 false，任务未完成")
            print(f"   当前值: {started}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 步行导航任务验证成功")
        print(f"   目的地: {destination}")
        print(f"   匹配到的答案: {matched_destination}")
        print(f"   导航方式: 步行")
        print(f"   已开始导航: {started}")

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
    print("指令 7 验证：步行导航去M+购物中心")
    print("=" * 60)

    # 执行验证
    success = verify_navigate_to_destination()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
