"""
Check Script Runner
===================
Run individual or all check scripts and output test results report.

Usage:
    python run_checks.py                    # Run all checks
    python run_checks.py 1                  # Run check script #1
    python run_checks.py 1 5 10             # Run specified check scripts
    python run_checks.py --range 1-10       # Run checks in range
    python run_checks.py --difficulty 1     # Run checks by difficulty
    python run_checks.py -d DEVICE_ID       # Specify device
"""

import importlib
import sys
import os
import json
import time
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import get_adb, get_ui


# Instruction to difficulty mapping
INSTRUCTIONS = {
    1:  ("Tell me how many likes the first post on the homepage has", 1),
    2:  ("Tell me how many likes the currently playing short video has", 1),
    3:  ("Tell me how many contacts are on the current messages page", 1),
    4:  ("Tell me the username of the current user", 1),
    5:  ("Like the first post on the homepage", 1),
    6:  ("Favorite the first post on the homepage", 1),
    7:  ("Open the notifications page", 1),
    8:  ("Go to the author profile of the first post on the homepage", 1),
    9:  ("Repost the first post", 1),
    10: ("Swipe to view the next short video", 1),
    11: ("Edit gender on profile to female", 2),
    12: ("Search for content related to 'happy' on the search page", 2),
    13: ("Open the first conversation on the messages page", 2),
    14: ("Show me the first comment of the first post on the homepage", 2),
    15: ("Share the first post on the homepage", 2),
    16: ("Share my personal QR code", 2),
    17: ("Mark the first post on the homepage as 'Not Interested'", 2),
    18: ("Check my number of followers", 2),
    19: ("Like the currently playing short video", 2),
    20: ("Check how many items are in my favorites collection", 2),
    21: ("Comment 'Nice!' under the second post on the homepage", 2),
    22: ("Open a chat and send the message 'Hello, how are you?'", 2),
    23: ("Set my account to private", 2),
    24: ("Set daily usage time limit to 60 minutes", 2),
    25: ("Change my username to 'zhou'", 2),
    26: ("Follow the author of the third post on the homepage", 2),
    27: ("Randomly select a user and block them", 2),
    28: ("Randomly add a close friend", 2),
    29: ("Remove a follower", 2),
    30: ("Enable Sleep Mode", 2),
    31: ("View the first video on my profile", 3),
    32: ("Log out of the current account", 3),
    33: ("Create a new collection named 'Favorites'", 3),
    34: ("Create a new post: select the second picture from the album, set title 'Beautiful sunset', add hashtag #nature, add location 'Central Park', then post", 3),
    35: ("Create a new post: select any picture, enter a title, add a poll with question 'Which is better?' and options 'Option A' and 'Option B', then post", 3),
    36: ("Create a new post: select any picture, enter a title, add a music track by search, set audience to 'Close Friends', then post", 3),
    37: ("Send 'I like your post!' to an unfollowed user", 3),
    38: ("Create a new post, hide like count, enable Facebook sharing", 3),
    39: ("Create a new post: select the second picture from the album, set title 'Beautiful sunset', add hashtag #nature, add location 'Central Park', hide like count, disable comments, then post", 3),
    40: ("Post a short video", 3),
}

DIFFICULTY_NAMES = {1: "Easy", 2: "Medium", 3: "Hard"}


def run_single_check(check_id, adb, ui=None):
    """Run a single check script"""
    module_name = f"check_{check_id:02d}"
    try:
        mod = importlib.import_module(module_name)
        if ui is None:
            ui = get_ui(adb)
        passed, msg = mod.check(adb, ui)
        return {"id": check_id, "passed": passed, "message": msg}
    except Exception as e:
        return {"id": check_id, "passed": False, "message": f"Script execution error: {e}"}


def run_checks(check_ids, device_id=None):
    """Run multiple check scripts"""
    adb = get_adb(device_id)
    results = []

    print(f"\n{'='*60}")
    print(f"  Instagram Simulator Test Report")
    print(f"  Total {len(check_ids)} checks")
    print(f"{'='*60}\n")

    for cid in check_ids:
        instruction, difficulty = INSTRUCTIONS.get(cid, (f"Unknown instruction #{cid}", 0))
        diff_name = DIFFICULTY_NAMES.get(difficulty, "?")
        print(f"[#{cid:02d}] ({diff_name}) {instruction}")

        ui = get_ui(adb)
        result = run_single_check(cid, adb, ui)
        results.append(result)

        status = "PASS" if result["passed"] else "FAIL"
        print(f"  -> [{status}] {result['message']}\n")

    # Summary
    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed
    print(f"\n{'='*60}")
    print(f"  Test Summary")
    print(f"{'='*60}")
    print(f"  Total: {len(results)}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    if results:
        print(f"  Pass Rate: {passed/len(results)*100:.1f}%")

    # Statistics by difficulty
    for diff in [1, 2, 3]:
        diff_results = [r for r in results if INSTRUCTIONS.get(r["id"], (None, 0))[1] == diff]
        if diff_results:
            dp = sum(1 for r in diff_results if r["passed"])
            print(f"  {DIFFICULTY_NAMES[diff]}: {dp}/{len(diff_results)}")

    # Failed items details
    failed_results = [r for r in results if not r["passed"]]
    if failed_results:
        print(f"\n  Failed Items:")
        for r in failed_results:
            print(f"    #{r['id']:02d}: {r['message']}")

    print(f"{'='*60}\n")

    return results


def main():
    parser = argparse.ArgumentParser(description="Instagram Simulator Check Script Runner")
    parser.add_argument("ids", nargs="*", type=int, help="Check script numbers (1-40)")
    parser.add_argument("-d", "--device", help="ADB device ID")
    parser.add_argument("--range", help="Check range, e.g. 1-10")
    parser.add_argument("--difficulty", type=int, choices=[1, 2, 3], help="Filter by difficulty")
    parser.add_argument("--output", "-o", help="Output JSON report path")

    args = parser.parse_args()

    # Determine which check IDs to run
    check_ids = []
    if args.ids:
        check_ids = args.ids
    elif args.range:
        start, end = map(int, args.range.split("-"))
        check_ids = list(range(start, end + 1))
    elif args.difficulty:
        check_ids = [cid for cid, (_, diff) in INSTRUCTIONS.items() if diff == args.difficulty]
    else:
        check_ids = list(range(1, 41))

    # Filter valid IDs
    check_ids = [cid for cid in check_ids if 1 <= cid <= 40]

    if not check_ids:
        print("No valid check script IDs")
        sys.exit(1)

    results = run_checks(check_ids, args.device)

    # Output JSON report
    if args.output:
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "failed": sum(1 for r in results if not r["passed"]),
            "results": results,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()
