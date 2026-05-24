TASK12_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取完成设计稿的人名。",
    "properties": {
        "person_name": {
            "type": "string",
            "description": "完成设计稿的人名，仅输出姓名，不含称呼或头衔。",
        }
    },
    "required": ["person_name"],
    "additionalProperties": False,
}


def task12_validate_design_draft_person(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("person_name") == "周浩然":
        return True
    return False
