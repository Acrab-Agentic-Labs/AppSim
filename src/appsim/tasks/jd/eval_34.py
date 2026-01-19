import json
import os
import subprocess


def validate_task_thirty_four(result=None, device_id=None, backup_dir=None):
    """ 验证任务三十四：将陈七地址详情中的电话号码改成18972746987。 """

    addresses_file_path = os.path.join(backup_dir, "addresses.json") if backup_dir else "addresses.json"

    # 从设备拉取地址文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/addresses.json"])

    try:
        with open(addresses_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling addresses.json from device: {e}")
        return False

    # 读取并验证地址文件
    try:
        with open(addresses_file_path, "r", encoding="utf-8") as f:
            addresses = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error reading or parsing addresses.json")
        return False

    if not isinstance(addresses, list):
        print("Validation Failed: addresses.json is not a list.")
        return False

    # 查找指定ID的地址
    target_address = None
    for address in addresses:
        if isinstance(address, dict) and address.get("id") == "addr_005":
            target_address = address
            break

    if not target_address:
        print("Validation Failed: Address with id 'addr_005' not found.")
        return False

    # 验证电话号码
    expected_phone = "18972746987"
    actual_phone = target_address.get("phoneNumber")

    if actual_phone == expected_phone:
        print("Validation Success: Phone number for address 'addr_005' was correctly updated.")
        return True
    else:
        print(f"Validation Failed: Phone number is incorrect. Expected: '{expected_phone}', Actual: '{actual_phone}'")
        return False

if __name__ == "__main__":
    result = validate_task_thirty_four()
    print(f"__result__:{result}")