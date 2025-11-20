import json
import subprocess
import os


def validate_task_one(result=None, device_id=None, backup_dir=None):
    """验证任务一：在首页中搜索「iPhone 15」，并查看搜索结果的第一个商品"""
    task_one_logs_file_path = os.path.join(backup_dir, 'task_one_logs.json') if backup_dir else 'task_one_logs.json'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/task_one_logs.json'])
    subprocess.run(cmd, stdout=open(task_one_logs_file_path, 'w'))

    try:
        with open(task_one_logs_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # task_one_logs.json是TaskOneLog的数组，取最后一条
            if isinstance(data, list):
                data = data[-1] if data else {}
    except:
        return False

    # 检查action是否为TASK_COMPLETED
    if data.get('action') != 'TASK_COMPLETED':
        return False

    # TaskOneLog结构: details字段包含实际数据
    details = data.get('details', {})

    # 检查搜索关键词是否为iPhone 15
    if details.get('searchKeyword') != 'iPhone 15':
        return False

    # 检查查看的商品名称是否为iPhone 15 Pro Max 256GB
    if details.get('viewedProductName') != 'iPhone 15 Pro Max 256GB':
        return False

    return True


if __name__ == '__main__':
    result = validate_task_one()
    print(result)
