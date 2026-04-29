"""
指令 20 验证脚本：收藏所有周边1km以内（包括1km）的所有景点

答案：收藏4个景点
四个目标景点：
      - 庚子革命烈士墓宣道牌坊
      - 水生生物博物馆
      - 董必武纪念像
      - 烈士合葬墓

功能说明：
- 验证应用是否正确执行了收藏周边景点的任务
- 通过 ADB 读取应用私有存储中的 JSON 文件
- 检查 JSON 文件中是否包含必要的字段：attractions（景点列表）、favorited（是否已收藏）

验证逻辑：
1. 使用 ADB 读取 20_favorite_nearby_attractions.json 文件
2. 解析 JSON 内容
3. 验证 attractions 字段包含四个目标景点
4. 验证 favorited 字段为 true（表示已收藏）
5. 返回验证结果（PASS/FAIL）

步骤：10
"""

import json
import subprocess
import sys

# 预设的正确答案：四个目标景点
EXPECTED_ATTRACTIONS = [
    "庚子革命烈士墓墓道牌坊",
    "水生生物博物馆",
    "董必武纪念像",
    "烈士合葬墓"
]


def verify_favorite_nearby_attractions(device_id=None):
    """
    验证收藏周边景点任务是否完成

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
            "files/20_favorite_nearby_attractions.json"  # JSON 文件路径
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
        if "attractions" not in json_data:
            print("❌ FAIL: 缺少 'attractions' 字段")
            return False

        if "favorited" not in json_data:
            print("❌ FAIL: 缺少 'favorited' 字段")
            return False

        # 获取字段值
        attractions = json_data["attractions"]
        favorited = json_data["favorited"]

        # 验证 attractions 是否为列表
        if not isinstance(attractions, list):
            print("❌ FAIL: 'attractions' 字段不是列表类型")
            print(f"   实际类型: {type(attractions)}")
            return False

        # 验证是否包含所有四个目标景点
        missing_attractions = []
        for expected in EXPECTED_ATTRACTIONS:
            if expected not in attractions:
                missing_attractions.append(expected)

        if missing_attractions:
            print("❌ FAIL: 缺少以下目标景点：")
            for attraction in missing_attractions:
                print(f"   - {attraction}")
            print(f"\n   实际收藏的景点: {attractions}")
            return False

        # 验证是否已收藏
        if not favorited:
            print("❌ FAIL: 'favorited' 字段为 false，任务未完成")
            print(f"   当前值: {favorited}")
            return False

        # 验证通过，输出结果
        print("✓ PASS: 收藏周边景点任务验证成功")
        print(f"   收藏的景点数量: {len(attractions)}")
        print(f"   收藏的景点列表:")
        for attraction in attractions:
            print(f"      - {attraction}")
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
    print("指令 20 验证：收藏所有周边1km以内的所有景点")
    print("=" * 60)

    # 执行验证
    success = verify_favorite_nearby_attractions()

    # 输出最终结果
    print("=" * 60)
    if success:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败")
        sys.exit(1)
