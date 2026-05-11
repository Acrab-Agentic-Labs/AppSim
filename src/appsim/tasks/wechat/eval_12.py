import re


# 12、查看工作讨论组的消息，是谁完成了设计稿？把你的答案放置在<ans>和</ans>之间，你的答案必须是人名。


def task12_validate_design_draft_person(result=None, device_id=None, backup_dir=None):
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

        return match.group(1).strip() == "周浩然"
    except Exception:
        return False


if __name__ == "__main__":
    result = task12_validate_design_draft_person()
    print(result)
