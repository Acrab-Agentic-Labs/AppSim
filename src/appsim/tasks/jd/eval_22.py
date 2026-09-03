import re

TASK22_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取评价iPhone15电池续航强的评论数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "评价电池续航强的评论数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_matching_product_review_count(result=None, device_id=None, backup_dir=None):
    """验证任务：查看评价iPhone15电池续航强的评论有多少。"""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("count") == 1899


if __name__ == "__main__":
    pass