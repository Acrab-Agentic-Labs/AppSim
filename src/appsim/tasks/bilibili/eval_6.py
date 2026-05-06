import subprocess
import json
import os
import re

def validate_task_6(result=None, device_id=None, backup_dir=None):
    """
    任务6: 看看会员购里的商品全部买下来要多少钱
    改进: 从APP数据源获取商品数据并计算总价
    """
    if result is None:
        return False

    final_msg = result.get("final_message") or ""  # final_message 可能为 None，统一按空字符串处理

    try:
        # 1. 使用 ADB 从设备拉取会员购商品数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.bilibili_sim",
                   "cat", "files/shop_products.json"])

        result_data = subprocess.run(
            cmd,
            capture_output=True,
            encoding='utf-8',
            errors='replace',
            text=True,
            timeout=10
        )

        # 保存数据到备份目录
        if backup_dir:
            shop_file_path = os.path.join(backup_dir, 'shop_products.json')
            with open(shop_file_path, 'w', encoding='utf-8') as f:
                f.write(result_data.stdout)

        # 检查命令是否成功执行
        if result_data.returncode != 0 or not result_data.stdout:
            print("⚠️ 无法读取会员购数据，回退验证")
            return '269.6' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 会员购数据格式错误，回退验证")
            return '269.6' in final_msg

        # 3. 计算所有商品的总价
        products_list = data.get("products", [])
        total_price = sum(product.get("price", 0) for product in products_list)

        # 4. 验证 final_message 中是否包含正确答案
        # 处理可能的格式：269.6、269.60、269.6元等
        if str(total_price) in final_msg or f"{total_price:.1f}" in final_msg or f"{total_price:.2f}" in final_msg:
            print(f"✓ 验证成功: 会员购商品总价 = {total_price}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={total_price}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '269.6' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '269.6' in final_msg

if __name__ == '__main__':
    result = validate_task_6()
    print(result)
