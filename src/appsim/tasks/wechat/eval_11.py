TASK11_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取完成财务报表的人员姓名。",
    "properties": {
        "person_name": {
            "type": "string",
            "minLength": 1,
            "description": "完成财务报表的人员姓名，只返回人名，不要附加解释。",
        }
    },
    "required": ["person_name"],
    "additionalProperties": False,
}


def task11_validate_financial_report_person(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("person_name") == "孙睿":
        return True
    return False
