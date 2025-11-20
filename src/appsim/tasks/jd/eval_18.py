import subprocess
import os


def validate_task_eighteen(result=None, device_id=None, backup_dir=None):
    """验证任务十八：取消我的nike待付款订单"""
    task_eighteen_log_file_path = os.path.join(backup_dir, 'task_eighteen_log.txt') if backup_dir else 'task_eighteen_log.txt'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/task_eighteen_log.txt'])
    subprocess.run(cmd, stdout=open(task_eighteen_log_file_path, 'w'))

    try:
        with open(task_eighteen_log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # 检查日志中是否包含关键操作，并且确认是取消order_012订单
    required_keywords = ['尝试取消订单', '订单取消成功']

    for keyword in required_keywords:
        if keyword not in content:
            return False

    # 检查是否取消的是order_012订单
    if 'order_012' in content and '尝试取消订单' in content:
        return True

    return False


if __name__ == '__main__':
    result = validate_task_eighteen()
    print(result)
