# AutoTest Main Runner
# Runs individual check scripts (check_1.py ~ check_40.py)
# Usage:
#   python check.py <task_id>          # Run single task (e.g., python check.py 1)
#   python check.py all                # Run all 40 tasks
#   python check.py all -o results.json # Save results to file

import json
import sys
import os
import importlib


def load_tasks():
    tasks_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
    with open(tasks_file, "r", encoding="utf-8") as f:
        return json.load(f)


def run_single_check(task_id, serial=None):
    """Import and run a single check module."""
    module_name = f"check_{task_id}"
    try:
        mod = importlib.import_module(module_name)
    except ImportError:
        return {"status": "error", "task_id": task_id, "message": f"Module {module_name} not found"}

    from check_common import AppChecker
    checker = AppChecker(serial)

    if not checker.is_app_running():
        return {"status": "error", "task_id": task_id, "message": "App is not running in foreground"}

    try:
        passed = mod.check(checker)
        return {"status": "pass" if passed else "fail", "task_id": task_id}
    except Exception as e:
        return {"status": "error", "task_id": task_id, "message": str(e)}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MySpotify GUI Agent Task Checker")
    parser.add_argument("task_id", nargs="?", default=None,
                        help="Task ID (1-40) or 'all' to run all checks")
    parser.add_argument("--serial", "-s", default=None,
                        help="Android device serial number")
    parser.add_argument("--output", "-o", default=None,
                        help="Output results to JSON file")
    args = parser.parse_args()

    if args.task_id is None:
        parser.print_help()
        print("\nExamples:")
        print("  python check.py 1              # Check single task")
        print("  python check.py all            # Check all tasks")
        print("  python check.py all -o results.json  # Save results to file")
        sys.exit(0)

    # Load task definitions
    tasks_data = load_tasks()
    tasks = tasks_data["tasks"]

    # Add script directory to path for imports
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    results = []

    if args.task_id.lower() == "all":
        print(f"\nRunning all {len(tasks)} task checks...\n")
        for task in tasks:
            tid = task["task_id"]
            instruction = task["instruction"]
            print(f"{'='*60}")
            print(f"Task {tid}: {instruction}")

            result = run_single_check(tid, args.serial)
            result["instruction"] = instruction

            status = result["status"]
            if status == "pass":
                print(f"  Result: PASS")
            elif status == "fail":
                print(f"  Result: FAIL")
            else:
                print(f"  Result: ERROR - {result.get('message', '')}")

            results.append(result)
    else:
        tid = int(args.task_id)
        task = next((t for t in tasks if t["task_id"] == tid), None)
        if task is None:
            print(f"Error: Task {tid} not found")
            sys.exit(1)

        print(f"Task {tid}: {task['instruction']}")
        result = run_single_check(tid, args.serial)
        result["instruction"] = task["instruction"]
        results.append(result)

        status = result["status"]
        if status == "pass":
            print(f"  Result: PASS")
        elif status == "fail":
            print(f"  Result: FAIL")
        else:
            print(f"  Result: ERROR - {result.get('message', '')}")

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")
    errors = sum(1 for r in results if r["status"] == "error")
    total = len(results)
    print(f"  Total: {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Errors: {errors}")
    if total > 0:
        print(f"  Pass Rate: {passed / total * 100:.1f}%")

    # Save results
    if args.output:
        output_data = {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": f"{passed / total * 100:.1f}%" if total > 0 else "0%"
            },
            "results": results
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if failed == 0 and errors == 0 else 1)


if __name__ == "__main__":
    main()
