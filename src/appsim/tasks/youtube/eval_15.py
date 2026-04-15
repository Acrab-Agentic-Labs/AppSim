import json
import os
import subprocess


def validate_task_fifteen(result=None, device_id=None, backup_dir=None):
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False
    normalized_message = final_message.lower()

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

    if "final_message" in result and (
        "2" in final_message or
        "two" in normalized_message
    ):
        return True
    else:
        return False

if __name__ == "__main__":
    print(validate_task_fifteen())
