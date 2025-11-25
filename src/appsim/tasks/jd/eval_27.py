import json
import subprocess

def validate_task_twenty_seven(result=None, device_id=None, backup_dir=None):
    """ 验证任务：找到我的待收货订单中购买件数最多的商品并确认收货。 """
    # 构建 adb 命令来拉取 orders.json 文件
    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    # 注意：这里的路径是应用在设备上的内部存储路径
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/orders.json'])

    try:
        # 执行命令并获取输出
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        orders_data = json.loads(process.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing orders.json from device: {e}")
        return False

    # 遍历订单数据，查找 order_025
    for order in orders_data:
        if order.get('id') == 'order_025':
            # 检查订单状态
            if order.get('status') == 'PENDING_SHIPMENT':
                print("Validation successful: Order 'order_025' status is 'PENDING_SHIPMENT'.")
                return True
            else:
                print(f"Validation failed: Order 'order_025' status is '{order.get('status')}', not 'PENDING_SHIPMENT'.")
                return False

    print("Validation failed: Order 'order_025' not found in orders.json.")
    return False

if __name__ == '__main__':
    result = validate_task_twenty_seven()
    print(result)
