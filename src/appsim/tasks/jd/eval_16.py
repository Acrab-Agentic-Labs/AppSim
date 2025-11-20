import subprocess
import os


def validate_task_sixteen(result=None, device_id=None, backup_dir=None):
    """验证任务十六：搜索iPhone15，将iPhone15 黑色 256GB加入购物车后，选择微信支付，满3000减50优惠券结算"""
    task_sixteen_log_file_path = os.path.join(backup_dir, 'task_sixteen_log.txt') if backup_dir else 'task_sixteen_log.txt'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/task_sixteen_log.txt'])
    subprocess.run(cmd, stdout=open(task_sixteen_log_file_path, 'w'))

    try:
        with open(task_sixteen_log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # 检查日志中是否包含这两行关键信息
    line1 = '任务十六完成：已成功搜索iPhone15，筛选价格范围和手机类别，将iPhone15 黑色 256GB加入购物车，选择微信支付和满3000减50优惠券完成结算'
    line2 = '选择优惠券：满3000减50，优惠金额：¥50.0'

    if line1 in content and line2 in content:
        return True

    return False


if __name__ == '__main__':
    result = validate_task_sixteen()
    print(result)
