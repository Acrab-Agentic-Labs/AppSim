"""
音乐App自动化测试验证函数
用于验证各项任务是否成功完成
"""

import json
import os
import subprocess

# App包名
APP_PACKAGE = "com.example.netease_cloud_music_sim"


def read_json_from_device(file_path, device_id=None, result=None, backup_dir=None):
    """
    从设备读取JSON文件
    :param file_path: 设备上的文件路径(相对于app私有目录)
    :param backup_dir: 本地备份目录,用于存储从设备拉取的文件
    :return: JSON数据或None
    """
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", APP_PACKAGE, "cat", f"files/{file_path}"])

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}")
        return None

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        print(f"读取文件失败: {file_path}, adb返回码: {completed.returncode}, 错误: {stderr}")
        return None

    raw_data = completed.stdout.strip()
    if not raw_data:
        print(f"读取文件失败: {file_path}, 错误: 文件内容为空")
        return None

    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError as e:
        print(f"读取文件失败: {file_path}, JSON解析错误: {e}")
        return None

    if backup_dir:
        os.makedirs(backup_dir, exist_ok=True)
        local_file = os.path.join(backup_dir, os.path.basename(file_path))
        with open(local_file, "w", encoding="utf-8") as f_out:
            f_out.write(raw_data)

    return data


def _joined_text(data, keys):
    if not isinstance(data, dict):
        return ""
    return " ".join(str(data.get(key, "")) for key in keys if data.get(key))


def is_daily_recommend_song(current_song):
    """判断当前歌曲是否来自每日推荐。"""
    text = _joined_text(current_song, ["source", "sourceDetail", "sourceName", "from", "fromName"]).lower()
    if not text:
        return False

    normalized = text.replace("_", " ").replace("-", " ")
    return (
        "daily_recommend" in text
        or ("daily" in normalized and "recommend" in normalized)
        or "每日推荐" in text
        or "日推" in text
    )


def is_daily_recommend_context(state):
    """判断状态数据是否表示当前在每日推荐页面/歌单中。"""
    if not isinstance(state, dict):
        return False

    keys = [
        "currentViewingPlaylist",
        "currentPlaylist",
        "viewingPlaylist",
        "playlistContext",
        "currentPage",
        "currentScreen",
        "currentView",
        "page",
        "screen",
    ]
    text = _joined_text(state, keys).lower()
    normalized = text.replace("_", " ").replace("-", " ")
    return (
        "daily_recommend" in text
        or ("daily" in normalized and "recommend" in normalized)
        or "每日推荐" in text
        or "日推" in text
    )


def is_in_daily_recommend_context(playback_state):
    """判断当前播放上下文是否在每日推荐页面/歌单中。"""
    if not isinstance(playback_state, dict):
        return False

    if is_daily_recommend_context(playback_state):
        return True

    # 检查播放上下文
    context_keys = ["playbackContext", "context", "playContext"]
    for key in context_keys:
        ctx = playback_state.get(key)
        if is_daily_recommend_context(ctx):
            return True

    return False


def is_previous_action_value(value):
    """判断动作字段是否表示切换上一首。"""
    if value is None:
        return False
    normalized = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    previous_values = {
        "previous",
        "prev",
        "previous_song",
        "prev_song",
        "skip_previous",
        "上一首",
        "切换上一首",
    }
    return normalized in previous_values or "上一首" in normalized


def has_previous_action(record):
    """在状态或记录对象中查找上一首动作证据。"""
    if not isinstance(record, dict):
        return False

    action_keys = [
        "lastAction",
        "recentAction",
        "lastPlaybackAction",
        "playbackAction",
        "action",
        "type",
        "event",
        "operation",
    ]
    if any(is_previous_action_value(record.get(key)) for key in action_keys):
        return True

    for value in record.values():
        if isinstance(value, dict) and has_previous_action(value):
            return True
        if isinstance(value, list) and any(has_previous_action(item) for item in value[-3:]):
            return True
    return False
