"""
Check Script #12: Search for content related to "happy" on the search page
Difficulty: 2 (Medium)
Check Method: Read exported search_state.json and verify query/results
"""
import json
import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def _read_search_state(adb):
    cmd = adb.base_cmd + [
        "exec-out",
        "run-as",
        APP_PACKAGE,
        "cat",
        "files/autotest/search_state.json",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0 or not result.stdout.strip():
            return None
        return json.loads(result.stdout)
    except Exception:
        return None


def check(adb, ui):
    state = _read_search_state(adb)
    if state:
        query = str(state.get("query", "")).strip().lower()
        is_searching = state.get("isSearching") is True
        total_results = int(state.get("totalResultsCount") or 0)
        post_results = int(state.get("postResultsCount") or 0)

        if query == "happy" and is_searching and total_results > 0:
            return result_pass(
                "Search state confirms happy query with results",
                {"query": query, "totalResultsCount": total_results, "postResultsCount": post_results},
            )

        return result_fail(
            "Search state does not confirm a completed happy search",
            state,
        )

    # Fallback UI check for older app builds without search_state.json
    all_texts = ui.get_all_texts()
    happy_count = sum(1 for t in all_texts if "happy" in t.lower())
    if happy_count >= 2 and (ui.has_text("Posts") or ui.has_text("Search results")):
        return result_pass("Search results contain 'happy' related content")

    if ui.has_text("Search") and ui.has_text("happy"):
        return result_fail("Search box has 'happy' but no search results/state found")

    return result_fail("Not on search results page for happy")


if __name__ == "__main__":
    run_check(check)
