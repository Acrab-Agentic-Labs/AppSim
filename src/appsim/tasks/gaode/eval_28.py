"""
指令 28 验证脚本：完成路线导航：M+购物中心到武汉市人民政府再到芦苇滩最后到我的位置的路线导航

答案：站点顺序为 M+购物中心 -> 武汉市人民政府 -> 芦苇滩 -> 我的位置

功能说明：
- 验证应用是否正确执行了多站点路线导航任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：stops（站点数组）、completed（是否已完成）

验证逻辑：
1. 使用 ADB 读取 29_multi_stop_navigation.json 文件
2. 解析 JSON 内容
3. 验证 stops 数组按顺序包含：M+购物中心、武汉市人民政府、芦苇滩、我的位置
4. 验证站点顺序不能错误
5. 验证 completed 字段为 true（表示已完成路线导航）
6. 返回验证结果（PASS/FAIL）
"""

import json
import subprocess
import sys

# 预设的正确答案（按顺序的站点）
EXPECTED_STOPS_ORDER = ["M+", "武汉市人民政府", "芦苇滩", "我的位置"]


def verify_multi_stop_navigation_completed(device_id=None):
    """
    验证多站点路线导航任务是否完成

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
            "files/29_multi_stop_navigation.json"  # JSON 文件路径
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
        if "stops" not in json_data:
            print("❌ FAIL: 缺少 'stops' 字段")
            return False

        if "completed" not in json_data:
            print("❌ FAIL: 缺少 'completed' 字段")
            return False

        # 获取字段值
        stops = json_data["stops"]
        completed = json_data["completed"]

        # 验证stops是否为数组
        if not isinstance(stops, list):
            print("❌ FAIL: 'stops' 字段不是数组")
            print(f"   当前类型: {type(stops).__name__}")
            return False

        # 验证站点数量
        if len(stops) < 4:
            print("❌ FAIL: 站点数量不足（需要至少4个）")
            print(f"   当前数量: {len(stops)}")
            print(f"   实际stops: {stops}")
            return False

        # 将stops转换为字符串列表
        stops_str_list = [str(stop) for stop in stops]

        # 验证每个站点的顺序
        for i, expected_stop in enumerate(EXPECTED_STOPS_ORDER):
            if i >= len(stops):
                print(f"❌ FAIL: 缺少第{i+1}个站点")
                print(f"   预期第{i+1}个站点: {expected_stop}")
                print(f"   实际stops: {stops}")
                return False

            if expected_stop not in stops_str_list[i]:
                print(f"❌ FAIL: 第{i+1}个站点顺序错误")
                print(f"   预期第{i+1}个站点: {expected_stop}")
                print(f"   实际第{i+1}个站点: {stops[i]}")
                print(f"   完整站点列表: {stops}")
                return False

        # 验证是否已完成路线导航
        if not completed:
            print("❌ FAIL: 'completed' 字段为 false，任务未完成")
            print(f"   当前值: {completed}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 多站点路线导航任务验证成功")
        print(f"   站点列表: {stops}")
        print(f"   已完成: {completed}")

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
    print("指令 28 验证：完成路线导航：M+购物中心到武汉市人民政府再到芦苇滩最后到我的位置")
    print("=" * 60)

    # 执行验��
    success = verify_multi_stop_navigation_completed()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
