import json
import subprocess
import os


def validate_task_nineteen(result=None, device_id=None, backup_dir=None):
    """验证任务十九：新建默认地址"代嘉仪，13066666666 湖北省武汉市洪山区文秀街9号"并设为默认地址"""
    addresses_file_path = os.path.join(backup_dir, 'addresses.json') if backup_dir else 'addresses.json'

    cmd = ['adb']
    if device_id:
        cmd.extend(['-s', device_id])
    cmd.extend(['exec-out', 'run-as', 'com.example.MyJD', 'cat', 'files/persistent_data/addresses.json'])
    subprocess.run(cmd, stdout=open(addresses_file_path, 'w'))

    try:
        with open(addresses_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # addresses.json是Address的数组
            addresses = data if isinstance(data, list) else []
    except:
        return False

    # 检查地址列表中是否包含"代嘉仪，13066666666，湖北省武汉市江夏区文秀街9号"且为默认地址
    for address in addresses:
        if isinstance(address, dict):
            recipient_name = address.get('recipientName', '')
            phone_number = address.get('phoneNumber', '')
            province = address.get('province', '')
            city = address.get('city', '')
            district = address.get('district', '')
            detail_address = address.get('detailAddress', '')
            is_default = address.get('isDefault', False)

            # 检查是否匹配：代嘉仪，13066666666，湖北省武汉市江夏区文秀街9号
            if (recipient_name == '代嘉仪' and
                phone_number == '13066666666' and
                province == '湖北省' and
                city == '武汉市' and
                district == '江夏区' and
                '文秀街9号' in detail_address and
                is_default):
                return True

    return False


if __name__ == '__main__':
    result = validate_task_nineteen()
    print(result)
