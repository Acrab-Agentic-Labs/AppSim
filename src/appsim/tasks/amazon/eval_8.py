import json
import os
import subprocess

# 初始地址种子（AppSim-Amazon 的 assets/data/addresses.json: addr_001 ~ addr_012）
BASELINE_ADDRESS_IDS = {f"addr_{index:03d}" for index in range(1, 13)}
TARGET_ADDRESS_ID = "addr_004"


def verify_shipping_address_deleted(result=None, device_id=None, backup_dir=None):
    """Validate task 8: delete the fourth shipping address (addr_004), leaving the others intact."""
    addresses_file_path = os.path.join(backup_dir, "addresses.json") if backup_dir else "addresses.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/addresses.json"])
    subprocess.run(cmd, stdout=open(addresses_file_path, "w"))

    try:
        with open(addresses_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            addresses = data if isinstance(data, list) else []
    except Exception:
        return False

    remaining_ids = {
        address.get("id")
        for address in addresses
        if isinstance(address, dict) and address.get("id")
    }

    # 目标地址必须被删掉，且删除过程中不能连带其它初始地址
    if TARGET_ADDRESS_ID in remaining_ids:
        return False
    return not ((BASELINE_ADDRESS_IDS - {TARGET_ADDRESS_ID}) - remaining_ids)


if __name__ == "__main__":
    result = verify_shipping_address_deleted()
    print(result)
