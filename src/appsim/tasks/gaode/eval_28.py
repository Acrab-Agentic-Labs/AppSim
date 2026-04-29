"""
指令 28 验证脚本：在导航去M+购物中心的路线中添加第一个途经点芦苇滩，第二个途经点武汉市人民政府

答案：目的地为M+购物中心，途经点包含芦苇滩和武汉市人民政府

功能说明：
- 验证应用是否正确执行了在导航路线中添加多个途经点的任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：destination（目的地）、waypoints（途经点数组）、added（是否已添加）

验证逻辑：
1. 使用 ADB 读取 28_add_multiple_waypoints.json 文件
2. 解析 JSON 内容
3. 验证 destination 字段包含 "M+" 或 "M+购物中心"
4. 验证 waypoints 数组包含 "芦苇滩" 和 "武汉市人民政府"
5. 验证 added 字段为 true（表示已添加途经点）
6. 返回验证结果（PASS/FAIL）

步骤：13
"""

import json
import subprocess
import sys

# 预设的正确答案
EXPECTED_DESTINATION = ["M+", "M+购物中心"]
EXPECTED_WAYPOINTS = ["芦苇滩", "武汉市人民政府"]


def verify_add_multiple_waypoints(device_id=None):
    """
    验证添加多个途经点任务是否完成

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
            "files/28_add_multiple_waypoints.json"  # JSON 文件路径
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

        if "waypoints" not in json_data:
            print("❌ FAIL: 缺少 'waypoints' 字段")
            return False

        if "added" not in json_data:
            print("❌ FAIL: 缺少 'added' 字段")
            return False

        # 获取字段值
        destination = json_data["destination"]
        waypoints = json_data["waypoints"]
        added = json_data["added"]

        # 验证目的地是否包含预设答案中的任意一个
        found_dest_match = False
        matched_dest = None
        for expected in EXPECTED_DESTINATION:
            if expected in str(destination):
                found_dest_match = True
                matched_dest = expected
                break

        if not found_dest_match:
            print("❌ FAIL: 目的地中未包含预期答案")
            print(f"   预期答案（任意一个）: {', '.join(EXPECTED_DESTINATION)}")
            print(f"   实际结果: {destination}")
            return False

        # 验证waypoints是否为数组
        if not isinstance(waypoints, list):
            print("❌ FAIL: 'waypoints' 字段不是数组")
            print(f"   当前类型: {type(waypoints).__name__}")
            return False

        # 验证途经点数量
        if len(waypoints) < 2:
            print("❌ FAIL: 途经点数量不足（需要至少2个）")
            print(f"   当前数量: {len(waypoints)}")
            print(f"   实际waypoints: {waypoints}")
            return False

        # 将waypoints转换为字符串列表
        waypoints_str_list = [str(wp) for wp in waypoints]

        # 验证第一个途经点是否包含"芦苇滩"
        if "芦苇滩" not in waypoints_str_list[0]:
            print("❌ FAIL: 第一个途经点不是'芦苇滩'")
            print(f"   预期第一个途经点: 芦苇滩")
            print(f"   实际第一个途经点: {waypoints[0]}")
            return False

        # 验证第二个途经点是否包含"武汉市人民政府"
        if "武汉市人民政府" not in waypoints_str_list[1]:
            print("❌ FAIL: 第二个途经点不是'武汉市人民政府'")
            print(f"   预期第二个途经点: 武汉市人民政府")
            print(f"   实际第二个途经点: {waypoints[1]}")
            return False

        # 验证是否已添加途经点
        if not added:
            print("❌ FAIL: 'added' 字段为 false，任务未完成")
            print(f"   当前值: {added}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 添加多个途经点任务验证成功")
        print(f"   目的地: {destination}")
        print(f"   途经点: {waypoints}")
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
    print("指令 28 验证：在导航去M+购物中心的路线中添加第一个途经点芦苇滩，第二个途经点武汉市人民政府")
    print("=" * 60)

    # 执行验证
    success = verify_add_multiple_waypoints()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
