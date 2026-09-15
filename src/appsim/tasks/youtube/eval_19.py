TASK19_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total duration of videos in Liked videos.",
    "properties": {
        "duration": {
            "type": "string",
            "description": "The total duration in MM:SS or M:SS format (e.g., '8:00').",
        }
    },
    "required": ["duration"],
    "additionalProperties": False,
}


def verify_liked_videos_total_duration(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    duration = str(extracted_answer.get("duration") or "")
    return "8:00" in duration
