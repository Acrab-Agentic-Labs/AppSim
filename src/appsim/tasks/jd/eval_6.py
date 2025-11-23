import subprocess
import os
import json


def validate_task_six(result=None, device_id=None, backup_dir=None):
    """验证任务六：结算我的第一个待付款订单"""
    # 从设备中拉取订单文件
    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/orders.json'])

    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        orders_data = json.loads(process.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing orders.json: {e}")
        return False

    # 检查第一个订单的状态
    if orders_data:
        first_order = orders_data[0]
        if first_order.get('id') == 'order_008' and first_order.get('status') != 'PENDING_PAYMENT':
            return True

    return False


if __name__ == '__main__':
    result = validate_task_six()
    print(result)