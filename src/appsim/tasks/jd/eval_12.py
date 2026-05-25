import re

TASK12_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取商品送达所需的分钟数。",
    "properties": {
        "minutes": {
            "type": "integer",
            "description": "商品送达还需要多少分钟，必须是阿拉伯数字整数。",
        }
    },
    "required": ["minutes"],
    "additionalProperties": False,
}


def validate_task_twelve(result=None, device_id=None, backup_dir=None):
    """验证任务十二：查看京东秒送的物流消息，确定商品还有多少分钟能送达。"""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("minutes") == 30


if __name__ == "__main__":
    pass
