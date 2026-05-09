import re


# 5、看看幸福一家人群，确定一下周六几点集合？在哪集合？把你的答案放置在<ans>和</ans>之间，你的答案必须包含集合时间和集合地点。


def task5_validate_info_in_group(result=None, device_id=None, backup_dir=None):
    try:
        if not isinstance(result, dict):
            return False

        final_msg = result.get("final_message")
        if final_msg is None:
            return False

        final_msg = str(final_msg)
        match = re.search(
            r"<ans>\s*(.*?)\s*</ans>",
            final_msg,
            re.IGNORECASE | re.DOTALL,
        )
        if match is None:
            return False

        answer = re.sub(r"\s+", "", match.group(1))
        has_time = (
            "9点" in answer
            or "九点" in answer
            or "9:00" in answer
            or "9：00" in answer
            or "09:00" in answer
            or "09：00" in answer
        )
        has_location = "香山门口" in answer
        return has_time and has_location
    except Exception:
        return False


if __name__ == "__main__":
    result = task5_validate_info_in_group()
    print(result)
