import subprocess
import json
import os
import re

def validate_task_30(result=None, device_id=None, backup_dir=None):
    """
    任务30: 看一下会员购里的商品一共卖了多少件
    改进: 从APP数据源获取商品数据并统计总销量
    """
    if result is None:
        return False

    final_msg = result.get("final_message", "")

    try:
        # 1. 使用 ADB 从设备拉取会员购商品数据
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "bilibili_sim",
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
            return '4963' in final_msg

        # 2. 解析JSON数据
        try:
            data = json.loads(result_data.stdout)
        except json.JSONDecodeError:
            print("⚠️ 会员购数据格式错误，回退验证")
            return '4963' in final_msg

        # 3. 统计所有商品的总销量
        products_list = data.get("products", [])
        total_sales = sum(product.get("sales_count", 0) for product in products_list)

        # 4. 验证 final_message 中是否包含正确答案
        if str(total_sales) in final_msg:
            print(f"✓ 验证成功: 会员购商品总销量 = {total_sales}")
            return True
        else:
            print(f"❌ 验证失败: 期望答案={total_sales}, 实际回答={final_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ ADB命令超时，回退验证")
        return '4963' in final_msg
    except Exception as e:
        print(f"⚠️ 验证过程出错: {str(e)}, 回退验证")
        return '4963' in final_msg

if __name__ == '__main__':
    result = validate_task_30()
    print(result)

