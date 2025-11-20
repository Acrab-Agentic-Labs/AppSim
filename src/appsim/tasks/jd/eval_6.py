import subprocess
import os


def validate_task_six(result=None, device_id=None, backup_dir=None):
    """验证任务六：结算我的第一个待付款订单"""
    task_six_log_file_path = os.path.join(backup_dir, 'task_six_log.txt') if backup_dir else 'task_six_log.txt'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/task_six_log.txt'])
    subprocess.run(cmd, stdout=open(task_six_log_file_path, 'w'))

    try:
        with open(task_six_log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # 检查日志中是否包含关键信息
    required_keywords = [
        '点击付款按钮',
        '确认付款操作',
        '付款成功，订单ID: order_001'
    ]

    for keyword in required_keywords:
        if keyword not in content:
            return False

    return True


if __name__ == '__main__':
    result = validate_task_six()
    print(result)
