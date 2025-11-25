import json
import subprocess
import os

def validate_task_twenty_eight(result=None, device_id=None, backup_dir=None):
    """ 验证任务：找到购物车中单价最低的商品购买5件。 """

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

    # 1. 检查订单 (orders.json)
    orders = get_json_from_device('orders.json')
    if orders is None:
        return False # 如果无法读取文件，则验证失败

    # 查找最新的包含 "五常大米" 的订单
    new_wuchang_rice_order = None
    for order in sorted(orders, key=lambda x: x.get('createTime', 0), reverse=True):
        items = order.get('items', [])
        if any('五常大米' in item.get('product', {}).get('name', '') for item in items):
            new_wuchang_rice_order = order
            break

    if not new_wuchang_rice_order:
        print("Validation Failed: New order for '五常大米' not found.")
        return False

    # 检查订单项的数量和订单状态
    items = new_wuchang_rice_order.get('items', [])
    if not items:
        print("Validation Failed: '五常大米' order has no items.")
        return False

    # 假设五常大米是唯一或主要的订单项
    wuchang_rice_item = next((item for item in items if '五常大米' in item.get('product', {}).get('name', '')), None)

    if wuchang_rice_item and wuchang_rice_item.get('quantity') == 5 and new_wuchang_rice_order.get('status') == 'PENDING_RECEIPT':
        print("Validation Success: New order for '五常大米' found with quantity 5 and status PENDING_RECEIPT.")
        return True
    else:
        print("Validation Failed: '五常大米' order does not meet quantity or status requirements.")
        print(f"Actual quantity: {wuchang_rice_item.get('quantity') if wuchang_rice_item else 'N/A'}")
        print(f"Actual status: {new_wuchang_rice_order.get('status')}")
        return False


if __name__ == '__main__':
    result = validate_task_twenty_eight()
    print(result)
