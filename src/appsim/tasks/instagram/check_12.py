"""
Check Script #12: 搜索'happy'、点赞收藏第一条搜索结果、关注作者、给deepak.patel发'Great photos!'、添加亲密好友
Difficulty: 3 (Hard)
Check Method: Read search_state + posts_state + user_state + conversations_state
"""
import json
import subprocess
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *

INITIAL_FOLLOWING = ["user_anushka", "user_naina", "user_deepak", "user_yashi"]


def _read_search_state(adb):
    cmd = adb.base_cmd + [
        "exec-out", "run-as", APP_PACKAGE, "cat", "files/autotest/search_state.json",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0 or not result.stdout.strip():
            return None
        return json.loads(result.stdout)
    except Exception:
        return None


def check(adb, ui):
    # Search check
    search_ok = False
    state = _read_search_state(adb)
    if state:
        query = str(state.get("query", "")).strip().lower()
        is_searching = state.get("isSearching") is True
        if query == "happy" and is_searching:
            search_ok = True

    # Like + Save check on first post
    like_ok = False
    save_ok = False
    posts = get_posts_state(adb)
    if posts:
        original_posts = [p for p in posts if p["postId"].startswith("post_")]
        if original_posts:
            like_ok = "user_self" in original_posts[0].get("likedBy", [])
            save_ok = "user_self" in original_posts[0].get("savedBy", [])

    # Follow + close friend check
    user = get_user_state(adb)
    follow_ok = False
    close_friend_ok = False
    if user:
        current_following = user.get("following", [])
        new_follows = [u for u in current_following if u not in INITIAL_FOLLOWING]
        follow_ok = len(new_follows) > 0
        close_friend_ok = len(user.get("closeFriends", [])) > 0

    # Message check
    message_ok = False
    convs = get_conversations_state(adb)
    if convs and isinstance(convs, list):
        for conv in convs:
            if "user_deepak" in conv.get("participantIds", []):
                for msg in conv.get("messages", []):
                    if "Great photos!" in msg.get("text", ""):
                        message_ok = True
                        break
            if message_ok:
                break

    checks = {
        "search": search_ok,
        "like": like_ok,
        "save": save_ok,
        "follow": follow_ok,
        "message": message_ok,
        "close_friend": close_friend_ok,
    }

    missing = [k for k, v in checks.items() if not v]
    if not missing:
        return result_pass("All operations completed (search+like+save+follow+message+close_friend)")
    passed = [k for k, v in checks.items() if v]
    return result_fail(f"Partially completed. Done: {passed}, Missing: {missing}")


if __name__ == "__main__":
    run_check(check)
