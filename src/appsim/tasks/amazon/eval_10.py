import json
import os
import subprocess


def verify_store_followed(result=None, device_id=None, backup_dir=None):
    """Validate task 10: follow the Marshall store."""
    brands_file_path = os.path.join(backup_dir, "brands.json") if backup_dir else "brands.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/brands.json"])
    subprocess.run(cmd, stdout=open(brands_file_path, "w"))

    try:
        with open(brands_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            brands = data if isinstance(data, list) else []
    except:
        return False

    for brand in brands:
        if isinstance(brand, dict):
            if brand.get("brandName") == "Marshall":
                return brand.get("isFollowed") == True

    return False


if __name__ == "__main__":
    result = verify_store_followed()
    print(result)
