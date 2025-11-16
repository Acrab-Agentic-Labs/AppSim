import subprocess
import json


def BrowsingHistoryCheck(result=None, device_id=None):
    if result is None:
        return False

    if "final_message" not in result:
        return False
    if "收藏" and "秋冬" and "穿搭" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = BrowsingHistoryCheck()
    print(result)
