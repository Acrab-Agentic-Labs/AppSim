import json
import subprocess
import os


def validate_task_eighteen(result=None, device_id=None, backup_dir=None):
    """验证任务十八：取消我的nike待付款订单"""
    # Define the path for the orders file
    orders_file_path = os.path.join(backup_dir, 'orders.json') if backup_dir else 'orders.json'

    # Construct the adb command to pull the orders.json file from the device
    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/orders.json'])

    try:
        # Execute the command and capture the output
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        orders_data = json.loads(process.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing orders.json: {e}")
        return False

    # Check for order_012 and its status
    order_found = False
    for order in orders_data:
        if order.get('id') == 'order_012':
            order_found = True
            if order.get('status') == 'CANCELLED':
                return True
            else:
                return False # Found the order, but status is not CANCELLED

    # If order_012 was not found, it means it was deleted or never existed. This also means validation fails.
    return False


if __name__ == '__main__':
    result = validate_task_eighteen()
    print(result)