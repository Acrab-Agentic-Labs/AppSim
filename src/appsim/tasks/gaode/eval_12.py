#!/usr/bin/env python3
"""
Android App Chat Message Navigation Log Verification Script

This script verifies that the "发送与爸爸的聊天，询问吃了吗" action was correctly recorded
by reading the private storage JSON file using ADB.
"""

import json
import subprocess
import sys


def verify_last_log12(result=None, device_id=None):
    """
    Verify the last log entry in 12_dad_chat_history.json matches the expected action.

    Returns:
        bool: True if verification passes, False otherwise
    """
    try:
        # Use ADB to read the private file content directly into memory
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.GaoDe", "cat", "files/12_dad_chat_history.json"])

        result1 = subprocess.run(cmd, capture_output=True, text=False, check=True)

        # Decode the output with proper encoding handling
        try:
            stdout_text = result1.stdout.decode("utf-8")
        except UnicodeDecodeError:
            # Fallback to gbk encoding for Chinese Windows systems
            try:
                stdout_text = result1.stdout.decode("gbk")
            except UnicodeDecodeError:
                # Last resort: ignore decode errors
                stdout_text = result1.stdout.decode("utf-8", errors="ignore")

        # Parse JSON content from memory
        if not stdout_text.strip():
            print("FAIL: JSON file is empty")
            return False

        json_data = json.loads(stdout_text)

        # Check if there are any records
        if not json_data or len(json_data) == 0:
            print("FAIL: No records found in JSON file")
            return False

        # Get the last record
        last_record = json_data[-1]

        # Verify the action field
        if "action" not in last_record:
            print("FAIL: 'action' field not found in last record")
            return False

        expected_action = "发送与爸爸的聊天，询问吃了吗"
        actual_action = last_record["action"]
        if actual_action == expected_action:
            print("PASS: Dad chat message verification successful")
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
    # Verify the expected operation: "发送与爸爸的聊天，询问吃了吗"
    success = verify_last_log12()

    if success:
        print("\n✓ PASS")
        sys.exit(0)
    else:
        print("\n✗ FAIL")
        sys.exit(1)
