# Shared base module for all check scripts
# Provides AppChecker helper class with common UI inspection methods
# and JSON state reading from app private directory

import uiautomator2 as u2
import json
import subprocess
import sys


class AppChecker:
    """Helper class for UI state inspection via uiautomator2."""

    PACKAGE = "com.example.myspotify"

    def __init__(self, serial=None):
        self.serial = serial
        if serial:
            self.d = u2.connect(serial)
        else:
            self.d = u2.connect()

    def is_app_running(self):
        current = self.d.app_current()
        return current.get("package") == self.PACKAGE

    def find_text(self, text, timeout=3):
        return self.d(text=text).exists(timeout=timeout)

    def find_text_contains(self, text, timeout=3):
        return self.d(textContains=text).exists(timeout=timeout)

    def find_desc(self, desc, timeout=3):
        return self.d(description=desc).exists(timeout=timeout)

    def find_desc_contains(self, desc, timeout=3):
        return self.d(descriptionContains=desc).exists(timeout=timeout)

    def get_edit_text(self, timeout=3):
        el = self.d(className="android.widget.EditText")
        if el.exists(timeout=timeout):
            return el.get_text()
        return None

    def count_elements_by_text(self, text, timeout=3):
        els = self.d(text=text)
        if els.exists(timeout=timeout):
            return els.count
        return 0

    # ============ AutoTest JSON 状态读取 ============

    def read_json_from_device(self, filename):
        """
        从设备读取 autotest JSON 文件

        通过 adb exec-out run-as 读取应用私有目录中的 autotest/*.json

        Args:
            filename: JSON 文件名，如 "user_state.json"

        Returns:
            dict/list: 解析后的 JSON 数据，失败返回 None
        """
        try:
            cmd = ["adb"]
            if self.serial:
                cmd.extend(["-s", self.serial])
            cmd.extend([
                "exec-out", "run-as", self.PACKAGE,
                "cat", f"files/autotest/{filename}"
            ])

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode != 0 or not result.stdout.strip():
                return None

            return json.loads(result.stdout)
        except (json.JSONDecodeError, subprocess.TimeoutExpired, Exception) as e:
            print(f"Warning: Failed to read {filename} from device: {e}")
            return None

    def get_user_state(self):
        """读取用户状态（liked songs, followed artists 等）"""
        return self.read_json_from_device("user_state.json")

    def get_user_playlists(self):
        """读取用户创建的歌单"""
        return self.read_json_from_device("user_playlists.json")

    def get_playback_state(self):
        """读取播放状态"""
        return self.read_json_from_device("playback_state.json")

    # ============ 初始数据（已知默认值） ============

    # 应用初始状态（来自 user_data.json）
    INITIAL_LIKED_SONGS = ["song_001", "song_004"]
    INITIAL_FOLLOWED_ARTISTS = ["artist_001", "artist_002"]  # Taylor Swift, Ed Sheeran
    INITIAL_SAVED_PLAYLISTS = ["playlist_001", "playlist_002"]


def run_check(check_func, task_id):
    """Standard runner for a check function."""
    serial = sys.argv[1] if len(sys.argv) > 1 else None
    checker = AppChecker(serial)

    if not checker.is_app_running():
        result = {"status": "error", "task_id": task_id, "message": "App is not running in foreground"}
    else:
        try:
            passed = check_func(checker)
            result = {"status": "pass" if passed else "fail", "task_id": task_id}
        except Exception as e:
            result = {"status": "error", "task_id": task_id, "message": str(e)}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "pass" else 1)
