import json
import os
import subprocess


TASK15_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of search results for the query.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of search results. Must be an Arabic numeral integer.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def validate_task_fifteen(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    if not isinstance(count, int):
        return False

    state_path = os.path.join(backup_dir, "task_state.json") if backup_dir else "task_state.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.youtube_sim", "cat", "files/task_state.json"])
    subprocess.run(cmd, stdout=open(state_path, "w", encoding="utf-8"), stderr=subprocess.DEVNULL, check=False)

    try:
        state = json.load(open(state_path, "r", encoding="utf-8"))
    except Exception:
        return False

    searched = state.get("search_query", "").strip().lower() == "iphone"
    if not searched:
        for event in reversed(state.get("events", [])):
            if event.get("action") != "search_query_changed":
                continue
            if (event.get("details") or {}).get("query") == "iphone":
                searched = True
                break

    if not searched:
        return False

    return count == 2
