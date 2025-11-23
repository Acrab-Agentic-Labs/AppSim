import json
import subprocess
import os


def validate_task_seventeen(result=None, device_id=None, backup_dir=None):
    """验证任务十七：帮我在Apple京东自营店购买一件iPhone 15 粉色 256GB"""
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

    # Check the orders for the specific iPhone 15 purchase
    for order in orders_data:
        if order.get('status') == 'PENDING_RECEIPT':
            items = order.get('items', [])
            for item in items:
                product = item.get('product', {})
                product_name = product.get('name', '')
                selected_color = item.get('selectedColor', '')
                selected_version = item.get('selectedVersion', '')
                quantity = item.get('quantity', 0)

                # Check for the specific product details
                if ('iPhone 15' in product_name and
                        selected_color == '粉色' and
                        selected_version == '256GB' and
                        quantity == 1):
                    return True

    return False


if __name__ == '__main__':
    result = validate_task_seventeen()
    print(result)