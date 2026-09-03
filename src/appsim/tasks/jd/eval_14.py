import re

TASK14_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取华为商品中评论数最多的评论条数。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "华为商品评论数最多的为多少条，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_product_review_count(result=None, device_id=None, backup_dir=None):
    """验证任务十四：查看首页前十个商品中华为商品评论数最多的为多少条。"""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    return extracted_answer.get("count") == 3200


if __name__ == "__main__":
    pass
