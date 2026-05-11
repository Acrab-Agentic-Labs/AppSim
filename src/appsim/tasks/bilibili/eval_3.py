def validate_task_3(result=None, device_id=None, backup_dir=None):
    """
    任务3: 看看会员购里的前四个商品全部买下来要多少钱
    """
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    if 'final_message' in result and '269.6' in result['final_message']:
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_3()
    print(result)
