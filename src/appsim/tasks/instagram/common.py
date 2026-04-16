"""
Common Testing Utilities Module
Provides ADB interaction, UI parsing, screenshot and other basic functions
"""

import subprocess
import time
import re
import sys
import os
import json


class ADB:
    """ADB Controller"""

    def __init__(self, device_id=None):
        self.device_id = device_id
        self.base_cmd = ["adb"]
        if device_id:
            self.base_cmd += ["-s", device_id]

    def shell(self, cmd, timeout=30):
        full_cmd = self.base_cmd + ["shell", cmd]
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return ""
        except Exception as e:
            return f"ERROR: {e}"

    def get_ui_xml(self):
        self.shell("uiautomator dump /sdcard/ui_dump.xml")
        time.sleep(0.5)
        full_cmd = self.base_cmd + ["shell", "cat", "/sdcard/ui_dump.xml"]
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
            return result.stdout.strip()
        except Exception:
            return ""

    def tap(self, x, y):
        self.shell(f"input tap {x} {y}")
        time.sleep(0.5)

    def swipe(self, x1, y1, x2, y2, duration=300):
        self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
        time.sleep(0.5)

    def input_text(self, text):
        escaped = text.replace(" ", "%s").replace("'", "\\'")
        self.shell(f"input text '{escaped}'")
        time.sleep(0.3)

    def press_back(self):
        self.shell("input keyevent KEYCODE_BACK")
        time.sleep(0.5)

    def press_enter(self):
        self.shell("input keyevent KEYCODE_ENTER")
        time.sleep(0.3)

    def take_screenshot(self, local_path):
        self.shell("screencap -p /sdcard/screenshot.png")
        subprocess.run(self.base_cmd + ["pull", "/sdcard/screenshot.png", local_path],
                       capture_output=True, timeout=30)

    def clear_text(self, length=50):
        for _ in range(length):
            self.shell("input keyevent KEYCODE_DEL")
        time.sleep(0.3)

    def launch_app(self, package, activity=None):
        if activity:
            self.shell(f"am start -n {package}/{activity}")
        else:
            self.shell(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
        time.sleep(2)

    def force_stop(self, package):
        self.shell(f"am force-stop {package}")
        time.sleep(1)


class UI:
    """UI XML Parser"""

    def __init__(self, xml):
        self.xml = xml

    def has_text(self, text):
        """Check if screen contains specified text (case-insensitive)"""
        return text.lower() in self.xml.lower()

    def find_by_text(self, text):
        """Exact match for text attribute"""
        pattern = rf'<node[^>]*text="{re.escape(text)}"[^>]*/>'
        return re.findall(pattern, self.xml)

    def find_by_text_contains(self, text):
        """Fuzzy match for text attribute"""
        pattern = rf'<node[^>]*text="[^"]*{re.escape(text)}[^"]*"[^>]*/>'
        return re.findall(pattern, self.xml)

    def find_by_desc(self, desc):
        """Match content-desc attribute"""
        pattern = rf'<node[^>]*content-desc="[^"]*{re.escape(desc)}[^"]*"[^>]*/>'
        return re.findall(pattern, self.xml)

    def find_by_resource_id(self, rid):
        """Match resource-id attribute"""
        pattern = rf'<node[^>]*resource-id="[^"]*{re.escape(rid)}[^"]*"[^>]*/>'
        return re.findall(pattern, self.xml)

    def get_node_attr(self, node_str, attr):
        """Extract attribute value from node string"""
        match = re.search(rf'{attr}="([^"]*)"', node_str)
        return match.group(1) if match else None

    def get_node_bounds(self, node_str):
        """Extract center coordinates from node string"""
        bounds = self.get_node_attr(node_str, "bounds")
        if bounds:
            m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
            if m:
                x1, y1, x2, y2 = map(int, m.groups())
                return (x1 + x2) // 2, (y1 + y2) // 2
        return None, None

    def count_nodes_with_text(self, text):
        """Count nodes containing specified text"""
        return len(self.find_by_text_contains(text))

    def get_all_texts(self):
        """Extract all text attribute values"""
        return re.findall(r'text="([^"]*)"', self.xml)

    def get_all_descs(self):
        """Extract all content-desc attribute values"""
        return re.findall(r'content-desc="([^"]*)"', self.xml)


# Application package name
APP_PACKAGE = "com.example.myinstagram"
APP_ACTIVITY = ".MainActivity"


def get_adb(device_id=None):
    """Get ADB instance"""
    return ADB(device_id)


def get_ui(adb):
    """Get current UI parser"""
    xml = adb.get_ui_xml()
    return UI(xml)


def result_pass(msg):
    """Return pass result"""
    print(f"[PASS] {msg}")
    return True, msg


def result_fail(msg):
    """Return fail result"""
    print(f"[FAIL] {msg}")
    return False, msg


def result_info(msg):
    """Info output"""
    print(f"[INFO] {msg}")
    return msg


def run_check(check_func, device_id=None):
    """Common check execution entry point"""
    adb = get_adb(device_id)
    ui = get_ui(adb)
    passed, msg = check_func(adb, ui)
    return {"passed": passed, "message": msg}


def read_device_json(adb, file_path):
    """Read a JSON file from the app's private storage via adb.

    Args:
        adb: ADB instance
        file_path: File path relative to app's private storage (e.g. "files/autotest/user_state.json")

    Returns:
        Parsed JSON data (dict or list), or None if file not found or parse error
    """
    cmd = adb.base_cmd + ["exec-out", "run-as", APP_PACKAGE, "cat", file_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0 or "No such file" in result.stderr:
            return None
        return json.loads(result.stdout)
    except (json.JSONDecodeError, subprocess.TimeoutExpired, Exception):
        return None


def get_posts_state(adb):
    """Read posts state from device"""
    return read_device_json(adb, "files/autotest/posts_state.json")


def get_reels_state(adb):
    """Read reels state from device"""
    return read_device_json(adb, "files/autotest/reels_state.json")


def get_user_state(adb):
    """Read current user state from device"""
    return read_device_json(adb, "files/autotest/user_state.json")


def get_conversations_state(adb):
    """Read conversations state from device"""
    return read_device_json(adb, "files/autotest/conversations_state.json")


def get_new_post_events(adb):
    """Read new post creation events from device"""
    return read_device_json(adb, "files/autotest/new_post_events.json")


if __name__ == "__main__":
    adb = get_adb()
    ui = get_ui(adb)
    print("UI dump length:", len(ui.xml))
    print("All texts:", ui.get_all_texts()[:10])
