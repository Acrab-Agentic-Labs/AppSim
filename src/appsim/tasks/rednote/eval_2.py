import json
import subprocess


def BrowseNotesCheck(userId="user_current", expectedCount=3, result=None, device_id=None):
    """
    Check if user has browsed the expected number of notes
    Task 2: Scroll down and browse 3 recommended notes
    """
    # Get browsing history from device
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["adb", "exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"],
    )
    result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # Check if command executed successfully
    if result1.returncode != 0 or not result1.stdout:
        # print(f"❌ Failed to read browsing history file")
        # print(f"   Reason: ADB command failed (return code: {result1.returncode})")
        # if result1.stderr:
        # print(f"   Error: {result1.stderr}")
        return False

    # Parse JSON
    try:
        data = json.loads(result1.stdout)
    except:
        # print(f"❌ Failed to parse browsing history")
        # print(f"   Reason: Invalid JSON format")
        return False

    # Check browsing history
    try:
        # Check if data is empty
        if not data or len(data) == 0:
            # print(f"❌ Browsing history is empty")
            # print(f"   Reason: No browsing records found")
            # print(f"   Expected: At least {expectedCount} browsing records")
            return False

        # Get user's browsing records, sorted by time
        user_browsing = [item for item in data if item.get("userId") == userId]

        # Check if recent browsing count meets expectation
        if len(user_browsing) >= expectedCount:
            # Get the latest records
            recent_browsing = sorted(user_browsing, key=lambda x: x.get("browsedAt", ""), reverse=True)[:expectedCount]

            # Verify these records are from home feed
            home_feed_count = sum(1 for item in recent_browsing if item.get("sourceType") == "HOME_FEED")

            if home_feed_count >= expectedCount:
                # print(f"✓ Successfully browsed {expectedCount} notes from home feed")
                return True
            else:
                # print(f"❌ Not enough browsing records from home feed")
                # print(f"   Reason: Found {home_feed_count} home feed records, expected {expectedCount}")
                # print(f"   Total browsing records: {len(user_browsing)}")
                # Show source types of recent browsing
                source_types = [item.get("sourceType", "UNKNOWN") for item in recent_browsing]
                # print(f"   Source types of recent browsing: {source_types}")
                return False

        # print(f"❌ Not enough browsing records")
        # print(f"   Reason: User has only {len(user_browsing)} browsing record(s)")
        # print(f"   Expected: At least {expectedCount} browsing records")
        return False
    except Exception:
        # print(f"❌ Error while checking browsing history")
        # print(f"   Reason: {e}")
        return False


if __name__ == "__main__":
    print(
        BrowseNotesCheck(
            userId="user_current",  # Current user
            expectedCount=3,  # Browse 3 notes
        )
    )
