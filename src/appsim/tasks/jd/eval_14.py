def validate_task_fourteen(result=None, device_id=None):
    """验证任务十四：查看首页iPhone15商品共有多少条评论"""

    # 检查result中的final_message是否包含数字300的各种表达形式
    if result and "final_message" in result:
        message = result["final_message"]
        # 支持：300或三百
        patterns = ["300", "三百"]
        for pattern in patterns:
            if pattern in message:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_fourteen()
    print(result)
