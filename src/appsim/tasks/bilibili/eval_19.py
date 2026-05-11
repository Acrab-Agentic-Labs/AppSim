def validate_task_19(result=None, device_id=None, backup_dir=None):
    """
    任务19: 看一下会员购里的前四个商品一共卖了多少件
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '4963' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_19()
    print(result)
