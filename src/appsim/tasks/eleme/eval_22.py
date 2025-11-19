import json
import subprocess


# 验证任务22: 进入"我的"-"我的订单-待评价",找到已评价,删除最近的一个评价
# 关键验证点:
# 1. 必须进入评价中心页面
# 2. 必须切换到已评价标签
# 3. 必须删除评价
# 4. 必须有删除成功弹窗
def validate_delete_review(result=None, device_id=None):
    # 从设备获取文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.myele", "cat", "files/messages.json"])
    subprocess.run(cmd, stdout=open("messages.json", "w"))

    # 读取文件
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except:
        return False

    # 检查是否有数据
    if not all_data:
        return False

    # 检测1: 验证进入评价中心页面
    entered_reviews = False
    for record in all_data:
        if record.get("action") == "enter_reviews_page" and record.get("page") == "reviews":
            entered_reviews = True
            break

    if not entered_reviews:
        return False

    # 检测2: 验证切换到已评价标签
    switched_to_reviewed = False
    for record in all_data:
        if record.get("action") == "switch_to_reviewed" and record.get("page") == "reviews":
            extra_data = record.get("extra_data", {})
            if extra_data.get("selected_tab") == "已评价":
                switched_to_reviewed = True
                break

    if not switched_to_reviewed:
        return False

    # 检测3: 验证删除评价
    deleted_review = False
    for record in all_data:
        if record.get("action") == "delete_review" and record.get("page") == "reviews":
            extra_data = record.get("extra_data", {})
            # 检查是否删除成功
            if extra_data.get("deleted_successfully") == True:
                deleted_review = True
                break

    if not deleted_review:
        return False

    return True


if __name__ == "__main__":
    # 运行验证并输出结果
    result = validate_delete_review()
    print(result)
