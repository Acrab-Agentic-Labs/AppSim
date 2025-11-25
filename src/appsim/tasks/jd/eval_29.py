import json
import subprocess
import os

def validate_task_twenty_nine(result=None, device_id=None, backup_dir=None):
    """ 验证任务：结算总价低于2000的所有待付款订单。 """

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

    orders = get_json_from_device('orders.json')
    if orders is None:
        return False

    target_order_ids = ["order_009", "order_010", "order_012", "order_014", "order_015"]
    all_checked_pass = True

    orders_map = {order.get('id'): order for order in orders}

    for order_id in target_order_ids:
        order = orders_map.get(order_id)
        if order is None:
            print(f"Validation Failed: Order '{order_id}' not found in orders.json.")
            all_checked_pass = False
            break

        current_status = order.get('status')
        if current_status != 'PENDING_RECEIPT':
            print(f"Validation Failed: Order '{order_id}' status is '{current_status}', expected 'PENDING_RECEIPT'.")
            all_checked_pass = False
            break
        else:
            print(f"Order '{order_id}' status is correct: 'PENDING_RECEIPT'.")

    return all_checked_pass

if __name__ == '__main__':
    result = validate_task_twenty_nine()
    print(result)

