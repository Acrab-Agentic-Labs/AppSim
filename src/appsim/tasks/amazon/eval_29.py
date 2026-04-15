import json
import os
import subprocess


def validate_task_twenty_nine(result=None, device_id=None, backup_dir=None):
    """Validate task 29: find the product or products with the largest discount on the home page and follow their stores."""
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

    sony_followed = False
    cocacola_followed = False

    for brand in brands:
        if isinstance(brand, dict):
            brand_id = brand.get("brandId")
            if brand_id == "brand_sony":
                sony_followed = brand.get("isFollowed") == True
            elif brand_id == "brand_cocacola":
                cocacola_followed = brand.get("isFollowed") == True

    return sony_followed and cocacola_followed


if __name__ == "__main__":
    result = validate_task_twenty_nine()
    print(result)
