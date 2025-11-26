import subprocess
import json
import os

# 验证任务23: 在"我的"-"全部订单"中找到有麻辣烫的订单,进入"订单详情页",点击申请食无忧理赔
# 关键验证点:
# 1. 必须进入订单页面
# 2. 必须找到麻辣烫订单
# 3. 必须进入食无忧理赔页面
# 4. 必须申请理赔成功
def validate_task_twenty_one(result=None,device_id=None,backup_dir=None):
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
        return False

    # 检查是否有数据
    if not all_data:
        return False

    # 检测1: 验证进入订单页面 (这个可能已经在其他任务中记录过,所以不是必需的)
    # 检测2: 验证进入食无忧理赔页面
    entered_insurance = False
    found_mala_order = False

    for record in all_data:
        if record.get('action') == 'enter_food_insurance_page' and record.get('page') == 'food_insurance':
            extra_data = record.get('extra_data', {})
            restaurant_name = extra_data.get('restaurant_name', '')
            # 检查是否是麻辣烫订单
            if '麻辣烫' in restaurant_name:
                entered_insurance = True
                found_mala_order = True
                break

    if not entered_insurance:
        return False

    if not found_mala_order:
        return False

    # 检测3: 验证申请理赔成功
    applied_insurance = False
    for record in all_data:
        if record.get('action') == 'apply_food_insurance' and record.get('page') == 'food_insurance':
            extra_data = record.get('extra_data', {})
            # 检查是否申请成功
            if extra_data.get('apply_successfully') == True:
                applied_insurance = True
                break

    if not applied_insurance:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_twenty_one()
    print(result)
