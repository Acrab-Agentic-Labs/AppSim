"""
指令 10 验证脚本：收藏周边最近的餐馆

答案：肖记公安牛肉鱼杂馆

功能说明：
- 验证应用是否正确执行了收藏餐馆的任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：name（餐馆名称）、favorited（是否已收藏）

验证逻辑：
1. 使用 ADB 读取 10_favorite_nearest_restaurant.json 文件
2. 解析 JSON 内容
3. 验证 name 字段包含 "肖记公安牛肉鱼杂馆"
4. 验证 favorited 字段为 true（表示已收藏）
5. 返回验证结果（PASS/FAIL）

步骤：5
"""

import json
import subprocess
import sys

# 预设的正确答案
EXPECTED_RESTAURANT = "肖记公安牛肉鱼杂馆"


def verify_favorite_nearest_restaurant(device_id=None):
    """
    验证收藏餐馆任务是否完成

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
            "files/10_favorite_nearest_restaurant.json"  # JSON 文件路径
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

        if "favorited" not in json_data:
            print("❌ FAIL: 缺少 'favorited' 字段")
            return False

        # 获取字段值
        name = json_data["name"]
        favorited = json_data["favorited"]

        # 验证是否已收藏
        if not favorited:
            print("❌ FAIL: 'favorited' 字段为 false，任务未完成")
            print(f"   当前值: {favorited}")
            return False

        # 验证餐馆名称是否包含预设答案
        if EXPECTED_RESTAURANT not in str(name):
            print("❌ FAIL: 餐馆名称中未包含预期答案")
            print(f"   预期答案: {EXPECTED_RESTAURANT}")
            print(f"   实际结果: {name}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 收藏餐馆任务验证成功")
        print(f"   餐馆名称: {name}")
        print(f"   已收藏: {favorited}")

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
    print("指令 10 验证：收藏周边最近的餐馆")
    print("=" * 60)

    # 执行验证
    success = verify_favorite_nearest_restaurant()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
