import subprocess
import json
import os

def validate_task_seventeen(result=None,device_id=None,backup_dir=None):
    message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

    # 从设备获取文件
    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.myele', 'cat', 'files/messages.json'])
    subprocess.run(cmd, stdout=open(message_file_path, 'w'))

    # 读取文件
    try:
        with open(message_file_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
    except:
        all_data = []

    # 从数组中找到最后一个完成订单的记录
    order_record = None
    for record in reversed(all_data):
        if record.get('action') == 'complete_order':
            order_record = record
            break

    # 检测1: 验证完成订单操作存在
    if order_record is None:
        return False

    # 检测2: 验证page
    if order_record.get('page') != 'checkout':
        return False

    # 检测3: 验证extra_data存在
    if 'extra_data' not in order_record:
        return False

    extra_data = order_record['extra_data']

    # 检测4: 【关键】验证来自外卖页面
    if extra_data.get('from_page') != 'takeout':
        return False

    # 检测5: 【关键】验证支付成功
    if not extra_data.get('payment_success', False):
        return False

    # 检测6: 查找排序选择记录,验证选择了"距离优先"
    sort_record = None
    for record in reversed(all_data):
        if record.get('action') == 'select_sort_option':
            sort_record = record
            break

    if sort_record is None:
        return False

    # 检测7: 验证排序页面是外卖页面
    if sort_record.get('page') != 'takeout':
        return False

    # 检测8: 验证排序选项
    if 'extra_data' not in sort_record:
        return False

    sort_extra = sort_record['extra_data']
    if sort_extra.get('sort_option') != '距离优先':
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_seventeen()
    print(result)
