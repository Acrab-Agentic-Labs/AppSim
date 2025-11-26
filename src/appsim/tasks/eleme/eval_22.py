import subprocess
import json
import os

# 验证任务24: 在外卖页面筛选食无忧和预约配送,找一个商家给于骁和余味分别下一单明日中午到达的爆品
# 关键验证点:
# 1. 必须进入外卖页面
# 2. 必须筛选食无忧和预约配送
# 3. 必须给于骁和余味分别下单(两次订单,不同收货人)
# 4. 必须是明日到达
# 5. 配送时间必须在中午11点-13点之间
def validate_task_twenty_two(result=None,device_id=None,backup_dir=None):
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

    # 检测1: 验证进入外卖页面并使用筛选功能
    filtered_food_safety = False
    filtered_cross_day = False

    for record in all_data:
        if record.get('action') == 'apply_filter' and record.get('page') == 'takeout':
            extra_data = record.get('extra_data', {})
            filters = extra_data.get('filters', [])
            # 检查是否筛选了食无忧
            if 'FOOD_SAFETY' in filters or 'food_safety' in filters or '食无忧' in str(filters):
                filtered_food_safety = True
            # 检查是否筛选了跨天预定（预约配送）
            if 'CROSS_DAY_BOOKING' in filters or 'cross_day_booking' in filters or '跨天预订' in str(filters):
                filtered_cross_day = True

    if not filtered_food_safety:
        return False

    if not filtered_cross_day:
        return False

    # 检测2: 验证有两个不同地址的订单，且配送时间为明日中午
    order_addresses = []
    for record in all_data:
        if record.get('action') == 'complete_order' and record.get('page') == 'checkout':
            extra_data = record.get('extra_data', {})
            # 检查是否是明日配送
            delivery_date = extra_data.get('delivery_date')
            if not (delivery_date and '明日' in delivery_date):
                continue  # 跳过非明日的订单

            # 新增：检查配送时间是否在中午11-13点之间
            delivery_time_slot = extra_data.get('delivery_time_slot')  # 格式示例："11:30-12:00" 或 "12:30-13:00"
            if not delivery_time_slot:
                return False  # 无配送时间段信息

            try:
                start_time = delivery_time_slot.split('-')[0]  # 取时间段开始部分（如"11:30"）
                hour = int(start_time.split(':')[0])  # 提取小时（如11）
                # 验证小时是否在11点（含）到13点（不含）之间
                if hour < 11 or hour >= 13:
                    return False  # 不在中午时间段
            except (IndexError, ValueError):
                # 处理格式错误（如时间段拆分失败、小时转换失败）
                return False

            # 记录收货人信息
            address_name = extra_data.get('delivery_address_name', '')
            if address_name:
                order_addresses.append(address_name)


    # 检查是否有于骁和余味两个人的订单
    has_yuxiao = any('于骁' in addr for addr in order_addresses)
    has_yuwei = any('余味' in addr for addr in order_addresses)

    if not has_yuxiao:
        return False

    if not has_yuwei:
        return False

    # 检测3: 确认至少有两个订单（分别给两人）
    if len(order_addresses) < 2:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_twenty_two()
    print(result)
