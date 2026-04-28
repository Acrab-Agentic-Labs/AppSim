import re

# 任务25：进入"火车票"页面，查10月22日广州到杭州下午2点到5点的车次，检索这些车次中最高的价格
# 检查条件：智能体返回的价格是否为 470


def check_train_search_max_price(result=None, device_id=None):
    """
    验证任务25的最终答案。

    智能体可能返回一句自然语言，因此直接检查 final_message 中是否包含目标价格。
    """
    if result is None:
        return False

    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if "final_message" in result and (
        "470" in result["final_message"]
        or "470.0" in result["final_message"]
        or "￥470" in result["final_message"]
        or "470 元" in result["final_message"]
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    print("true" if check_train_search_max_price() else "false")
