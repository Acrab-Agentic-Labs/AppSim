from ..base import AppTasks, NumericReasoningCategory, TaskItem
from .eval_1 import verify_homepage_first_post_like_count
from .eval_2 import verify_current_reel_like_count
from .eval_3 import verify_message_contact_count
from .eval_4 import verify_current_username
from .eval_5 import verify_homepage_first_post_liked
from .eval_6 import verify_homepage_first_post_saved
from .eval_7 import verify_notifications_page_opened
from .eval_8 import verify_homepage_first_post_liked_saved_commented_reposted
from .eval_9 import verify_homepage_first_post_reposted
from .eval_10 import verify_next_reel_viewed
from .eval_11 import verify_profile_gender_updated
from .eval_12 import verify_search_post_actions_message_and_close_friend
from .eval_13 import verify_account_settings_updated
from .eval_14 import verify_homepage_first_post_comment_viewed
from .eval_15 import verify_homepage_first_post_share_opened
from .eval_16 import verify_personal_qr_code_share_opened
from .eval_17 import verify_homepage_first_post_marked_not_interested
from .eval_18 import verify_follower_count
from .eval_19 import verify_current_reel_liked
from .eval_20 import verify_saved_item_count
from .eval_21 import verify_homepage_second_post_commented
from .eval_22 import verify_chat_message_sent
from .eval_23 import verify_private_account_enabled
from .eval_24 import verify_daily_usage_limit_set
from .eval_25 import verify_username_changed
from .eval_26 import verify_homepage_third_post_author_followed
from .eval_27 import verify_user_blocked
from .eval_28 import verify_close_friend_added
from .eval_29 import verify_follower_removed
from .eval_30 import verify_sleep_mode_enabled
from .eval_31 import verify_profile_first_video_opened
from .eval_32 import verify_account_logged_out
from .eval_33 import verify_collection_created
from .eval_34 import verify_post_published_with_caption_hashtag_location
from .eval_35 import verify_post_published_with_poll
from .eval_36 import verify_post_published_with_music_and_audience
from .eval_37 import verify_video_post_published_with_location_and_audience
from .eval_38 import verify_post_published_with_like_count_hidden_and_facebook_sharing
from .eval_39 import verify_post_published_with_post_settings
from .eval_40 import verify_reel_published

import inspect

TASK1_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of likes on the first post.",
    "properties": {
        "like_count": {
            "type": "string",
            "description": "The like count (e.g. '123', '1.2K').",
        }
    },
    "required": ["like_count"],
    "additionalProperties": False,
}

TASK2_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of likes on the currently playing short video.",
    "properties": {
        "like_count": {
            "type": "string",
            "description": "The like count (e.g. '456', '2.3K').",
        }
    },
    "required": ["like_count"],
    "additionalProperties": False,
}

TASK3_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of contacts on the messages page.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The number of contacts/conversations.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}

TASK4_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the username of the current user.",
    "properties": {
        "username": {
            "type": "string",
            "description": "The current user's username.",
        }
    },
    "required": ["username"],
    "additionalProperties": False,
}

TASK18_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of followers.",
    "properties": {
        "follower_count": {
            "type": "string",
            "description": "The follower count (e.g. '100', '1.5K').",
        }
    },
    "required": ["follower_count"],
    "additionalProperties": False,
}

TASK20_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of items in the favorites collection.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The total number of items in the favorites/saved collection.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}

def build_instagram_verify_func(check_func):
    """Wrapper to convert check function to validate function signature"""
    def wrapper(result=None, device_id=None, backup_dir=None):
        from .common import get_adb, get_ui
        adb = get_adb(device_id)
        ui = get_ui(adb)
        try:
            sig = inspect.signature(check_func)
            if 'result' in sig.parameters:
                passed = check_func(adb, ui, result=result)
            else:
                passed = check_func(adb, ui)
            return passed
        except Exception:
            return False
    wrapper.__name__ = check_func.__name__
    return wrapper

INSTAGRAM_TASKS = AppTasks(
    package_name="com.example.myinstagram",
    task_items=[
        TaskItem(
            instruction="Tell me how many likes the first post on the homepage has",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_like_count),
            human_steps=1,
            evaluation_type="hybrid",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me how many likes the currently playing short video has",
            verify_func=build_instagram_verify_func(verify_current_reel_like_count),
            human_steps=1,
            evaluation_type="hybrid",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me how many contacts are on the current messages page",
            verify_func=build_instagram_verify_func(verify_message_contact_count),
            human_steps=1,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="hybrid",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me the username of the current user",
            verify_func=build_instagram_verify_func(verify_current_username),
            human_steps=1,
            evaluation_type="hybrid",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Like the first post on the homepage",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_liked),
            human_steps=2,
        ),
        TaskItem(
            instruction="Favorite the first post on the homepage",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_saved),
            human_steps=2,
        ),
        TaskItem(
            instruction="Open the notifications page",
            verify_func=build_instagram_verify_func(verify_notifications_page_opened),
            human_steps=2,
        ),
        TaskItem(
            instruction="Like the first post on the homepage, save it, comment 'Love this!', and repost it",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_liked_saved_commented_reposted),
            human_steps=8,
        ),
        TaskItem(
            instruction="Repost the first post",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_reposted),
            human_steps=2,
        ),
        TaskItem(
            instruction="Swipe to view the next short video",
            verify_func=build_instagram_verify_func(verify_next_reel_viewed),
            human_steps=2,
        ),
        TaskItem(
            instruction="Edit gender on profile to female",
            verify_func=build_instagram_verify_func(verify_profile_gender_updated),
            human_steps=4,
        ),
        TaskItem(
            instruction="Search for 'happy', like and save the first search result post, follow the author, send 'Great photos!' to deepak.patel, then add a close friend",
            verify_func=build_instagram_verify_func(verify_search_post_actions_message_and_close_friend),
            human_steps=17,
        ),
        TaskItem(
            instruction="Change username to 'Li', set gender to male, set account to private, and enable sleep mode",
            verify_func=build_instagram_verify_func(verify_account_settings_updated),
            human_steps=12,
        ),
        TaskItem(
            instruction="Show me the first comment of the first post on the homepage",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_comment_viewed),
            human_steps=2,
        ),
        TaskItem(
            instruction="Share the first post on the homepage",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_share_opened),
            human_steps=2,
        ),
        TaskItem(
            instruction="Share my personal QR code",
            verify_func=build_instagram_verify_func(verify_personal_qr_code_share_opened),
            human_steps=2,
        ),
        TaskItem(
            instruction="Mark the first post on the homepage as 'Not Interested'",
            verify_func=build_instagram_verify_func(verify_homepage_first_post_marked_not_interested),
            human_steps=3,
        ),
        TaskItem(
            instruction="Check my number of followers",
            verify_func=build_instagram_verify_func(verify_follower_count),
            human_steps=1,
            evaluation_type="hybrid",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Like the currently playing short video",
            verify_func=build_instagram_verify_func(verify_current_reel_liked),
            human_steps=2,
        ),
        TaskItem(
            instruction="Check how many items are in my favorites collection",
            verify_func=build_instagram_verify_func(verify_saved_item_count),
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="hybrid",
            answer_schema=TASK20_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Comment 'Nice!' under the second post on the homepage",
            verify_func=build_instagram_verify_func(verify_homepage_second_post_commented),
            human_steps=5,
        ),
        TaskItem(
            instruction="Open a chat with deepak.patel and send the message 'Hello, how are you?'",
            verify_func=build_instagram_verify_func(verify_chat_message_sent),
            human_steps=5,
        ),
        TaskItem(
            instruction="Set my account to private",
            verify_func=build_instagram_verify_func(verify_private_account_enabled),
            human_steps=4,
        ),
        TaskItem(
            instruction="Set daily usage time limit to 60 minutes",
            verify_func=build_instagram_verify_func(verify_daily_usage_limit_set),
            human_steps=5,
        ),
        TaskItem(
            instruction="Change my username to 'zhou'",
            verify_func=build_instagram_verify_func(verify_username_changed),
            human_steps=5,
        ),
        TaskItem(
            instruction="Follow the author of the third post on the homepage",
            verify_func=build_instagram_verify_func(verify_homepage_third_post_author_followed),
            human_steps=3,
        ),
        TaskItem(
            instruction="Randomly select a user and block them",
            verify_func=build_instagram_verify_func(verify_user_blocked),
            human_steps=5,
        ),
        TaskItem(
            instruction="Randomly add a close friend",
            verify_func=build_instagram_verify_func(verify_close_friend_added),
            human_steps=4,
        ),
        TaskItem(
            instruction="Remove a follower named deepak.patel",
            verify_func=build_instagram_verify_func(verify_follower_removed),
            human_steps=3,
        ),
        TaskItem(
            instruction="Enable Sleep Mode",
            verify_func=build_instagram_verify_func(verify_sleep_mode_enabled),
            human_steps=4,
        ),
        TaskItem(
            instruction="View the first video on my profile",
            verify_func=build_instagram_verify_func(verify_profile_first_video_opened),
            human_steps=3,
        ),
        TaskItem(
            instruction="Log out of the current account",
            verify_func=build_instagram_verify_func(verify_account_logged_out),
            human_steps=5,
        ),
        TaskItem(
            instruction="Create a new collection named 'Favorites'",
            verify_func=build_instagram_verify_func(verify_collection_created),
            human_steps=7,
        ),
        TaskItem(
            instruction="Create a new post: select the second picture from the album, set title 'Beautiful sunset', add hashtag #nature, add location 'Central Park', then post",
            verify_func=build_instagram_verify_func(verify_post_published_with_caption_hashtag_location),
            human_steps=10,
        ),
        TaskItem(
            instruction="Create a new post: select any picture, enter a title, add a poll with question 'Which is better?' and options 'Option A' and 'Option B', then post",
            verify_func=build_instagram_verify_func(verify_post_published_with_poll),
            human_steps=8,
        ),
        TaskItem(
            instruction="Create a new post: select any picture, enter a title, add a music track by search, set audience to 'Close Friends', then post",
            verify_func=build_instagram_verify_func(verify_post_published_with_music_and_audience),
            human_steps=12,
        ),
        TaskItem(
            instruction="Post a new video: select the second video from album, set caption 'cute', set location to 'Central Park', set audience to 'Close Friends', then post",
            verify_func=build_instagram_verify_func(verify_video_post_published_with_location_and_audience),
            human_steps=12,
        ),
        TaskItem(
            instruction="Create a new post, hide like count, enable Facebook sharing",
            verify_func=build_instagram_verify_func(verify_post_published_with_like_count_hidden_and_facebook_sharing),
            human_steps=9,
        ),
        TaskItem(
            instruction="Create a new post: select the second picture from the album, set title 'Beautiful sunset', add hashtag #nature, add location 'Central Park', hide like count, disable comments, then post",
            verify_func=build_instagram_verify_func(verify_post_published_with_post_settings),
            human_steps=13,
        ),
        TaskItem(
            instruction="Post a short video",
            verify_func=build_instagram_verify_func(verify_reel_published),
            human_steps=4,
        ),
    ],
)
