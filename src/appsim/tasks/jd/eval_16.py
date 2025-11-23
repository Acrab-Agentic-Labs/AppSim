import json
import subprocess
import os

def validate_task_sixteen(result=None, device_id=None, backup_dir=None):
    """验证任务十六：将购物车的iPhone15买下来，使用满3000减50的优惠券结算。"""

    def get_json_from_device(file_path):
        """从设备拉取并解析JSON文件。"""
        cmd = ['adb']
        if device_id:
            cmd.extend(['-s', device_id])
        cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', f'files/persistent_data/{file_path}'])
        try:
            process = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
            return json.loads(process.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading or parsing {file_path} from device: {e}")
            return None

    # 1. 检查购物车 (cart_items.json)
    cart_items = get_json_from_device('cart_items.json')
    if cart_items is None:
        return False  # 如果无法读取文件，则验证失败

    iphone_in_cart = any(
        'iPhone 15' in item.get('productName', '') for item in cart_items
    )
    if iphone_in_cart:
        print("Validation Failed: iPhone 15 is still in the cart.")
        return False

    # 2. 检查订单 (orders.json)
    orders = get_json_from_device('orders.json')
    if orders is None:
        return False # 如果无法读取文件，则验证失败

    # 查找最新的 iPhone 15 订单
    # 假设它是最新创建的订单，所以我们检查列表的第一个
    new_iphone_order = None
    for order in sorted(orders, key=lambda x: x.get('createTime', 0), reverse=True):
        items = order.get('items', [])
        if any('iPhone 15' in item.get('product', {}).get('name', '') for item in items):
            new_iphone_order = order
            break

    if not new_iphone_order:
        print("Validation Failed: New order for iPhone 15 not found.")
        return False

    # 验证订单金额是否正确应用了优惠券
    # 从订单项中获取成交价格
    expected_total_amount = sum(
        item.get('price', 0.0) * item.get('quantity', 0) for item in new_iphone_order.get('items', [])
    )
    actual_total_amount = new_iphone_order.get('totalAmount', 0.0)

    # 允许微小的浮点数误差
    if abs(expected_total_amount - actual_total_amount) > 0.01:
        print(f"Validation Failed: Order total is incorrect. Expected: {expected_total_amount}, Actual: {actual_total_amount}")
        return False

    print("Validation Success: iPhone 15 removed from cart and new order created with correct discount.")
    return True


if __name__ == '__main__':
    # For local testing, ensure the device is connected and the app state is correct.
    result = validate_task_sixteen()
    print(f"Validation Result: {result}")