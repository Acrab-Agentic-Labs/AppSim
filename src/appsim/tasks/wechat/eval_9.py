TASK9_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取歌曲名称。",
    "properties": {
        "song_name": {
            "type": "string",
            "description": "歌曲名称，仅输出歌名本身，不含引号或书名号。",
        }
    },
    "required": ["song_name"],
    "additionalProperties": False,
}


def verify_song_name_retrieved(result=None, device_id=None, backup_dir=None) -> bool:
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if isinstance(extracted_answer, dict) and extracted_answer.get("song_name") == "秋日私语":
        return True
    return False
