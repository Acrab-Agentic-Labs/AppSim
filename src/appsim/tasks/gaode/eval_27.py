"""
指令 27 验证脚本：在导航去滨江饭店的路线中添加收藏中第一行地点作为途径点

答案：目的地为滨江饭店，途经点为亚朵酒店

功能说明：
- 验证应用是否正确执行了在导航路线中添加收藏地点作为途经点的任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：destination（目的地）、waypoint（途经点）、added（是否已添加）

验证逻辑：
1. 使用 ADB 读取 27_add_favorite_as_waypoint.json 文件
2. 解析 JSON 内容
3. 验证 destination 字段包含 "滨江饭店"
4. 验证 waypoint 字段包含 "亚朵酒店"
5. 验证 added 字段为 true（表示已添加途经点）
6. 返回验证结果（PASS/FAIL）

步骤：10
"""

import json
import subprocess
import sys

# 预设的正确答案
EXPECTED_DESTINATION = "滨江饭店"
EXPECTED_WAYPOINT = "亚朵酒店"


def verify_add_favorite_as_waypoint(device_id=None):
    """
    验证添加收藏地点作为途经点任务是否完成

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
            "files/27_add_favorite_as_waypoint.json"  # JSON 文件路径
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

        if "waypoint" not in json_data:
            print("❌ FAIL: 缺少 'waypoint' 字段")
            return False

        if "added" not in json_data:
            print("❌ FAIL: 缺少 'added' 字段")
            return False

        # 获取字段值
        destination = json_data["destination"]
        waypoint = json_data["waypoint"]
        added = json_data["added"]

        # 验证目的地是否包含预设答案
        if EXPECTED_DESTINATION not in str(destination):
            print("❌ FAIL: 目的地中未包含预期答案")
            print(f"   预期答案: {EXPECTED_DESTINATION}")
            print(f"   实际结果: {destination}")
            return False

        # 验证途经点是否包含预设答案
        if EXPECTED_WAYPOINT not in str(waypoint):
            print("❌ FAIL: 途经点中未包含预期答案")
            print(f"   预期答案: {EXPECTED_WAYPOINT}")
            print(f"   实际结果: {waypoint}")
            return False

        # 验证是否已添加途经点
        if not added:
            print("❌ FAIL: 'added' 字段为 false，任务未完成")
            print(f"   当前值: {added}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 添加收藏地点作为途经点任务验证成功")
        print(f"   目的地: {destination}")
        print(f"   途经点: {waypoint}")
        print(f"   已添加: {added}")

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
    print("指令 27 验证：在导航去滨江饭店的路线中添加收藏中第一个地点作为途径点")
    print("=" * 60)

    # 执行验证
    success = verify_add_favorite_as_waypoint()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
