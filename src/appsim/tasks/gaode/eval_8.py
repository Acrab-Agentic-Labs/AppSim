#!/usr/bin/env python3
"""
Android App Banu Hotpot Selection Log Verification Script
"""

import json
import subprocess
import sys


def verify_last_log8(result=None, device_id=None):
    """
    Verify the last log entry in 8_banu_selection_history.json matches the expected action.
    """
    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.GaoDe", "cat", "files/8_banu_selection_history.json"])

        result1 = subprocess.run(cmd, capture_output=True, text=False, check=True)

        try:
            stdout_text = result1.stdout.decode("utf-8")
        except UnicodeDecodeError:
            try:
                stdout_text = result1.stdout.decode("gbk")
            except UnicodeDecodeError:
                stdout_text = result1.stdout.decode("utf-8", errors="ignore")

        if not stdout_text.strip():
            print("FAIL: JSON file is empty")
            return False

        json_data = json.loads(stdout_text)

        if not json_data or len(json_data) == 0:
            print("FAIL: No records found in JSON file")
            return False

        last_record = json_data[-1]

        if "action" not in last_record:
            print("FAIL: 'action' field not found in last record")
            return False

        expected_action = "搜索并选择巴奴火锅"
        actual_action = last_record["action"]
        if actual_action == expected_action:
            print("PASS: Banu hotpot selection action verification successful")
            print(f"Expected: {expected_action}")
            print(f"Actual: {actual_action}")
            print(f"Timestamp: {last_record.get('timestamp', 'N/A')}")
            print(f"Page: {last_record.get('page', 'N/A')}")
            return True
        else:
            print("FAIL: Action mismatch")
            print(f"Expected: {expected_action}")
            print(f"Actual: {actual_action}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"FAIL: ADB command failed - {e}")
        try:
            error_text = e.stderr.decode("utf-8") if e.stderr else "No error output"
        except:
            error_text = "Error decoding stderr"
        print(f"Error output: {error_text}")
        return False
    except json.JSONDecodeError as e:
        print(f"FAIL: JSON parsing error - {e}")
        print(f"Raw content: {stdout_text}")
        return False
    except Exception as e:
        print(f"FAIL: Unexpected error - {e}")
        return False


if __name__ == "__main__":
    success = verify_last_log8()

    if success:
        print("\n✓ PASS")
        sys.exit(0)
    else:
        print("\n✗ FAIL")
        sys.exit(1)
