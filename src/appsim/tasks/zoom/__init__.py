# All instructions: file index equals task index
# type: ignore
# noqa
from ..base import AppTasks, NumericReasoningCategory, TaskItem


from .eval_1 import verify_instant_meeting_invite_and_settings
from .eval_2 import verify_meeting_participation_and_chat_actions
from .eval_3 import verify_meeting_participant_controls_and_lock
from .eval_4 import verify_screen_sharing_pause_resume_and_chat
from .eval_5 import verify_meeting_media_state_and_chat
from .eval_6 import verify_scheduled_meeting_created_with_invite_settings
from .eval_7 import verify_recurring_meeting_created_with_participants
from .eval_8 import verify_scheduled_meeting_updated_with_participant_and_waiting_room
from .eval_9 import verify_scheduled_meeting_time_and_duration_updated
from .eval_10 import verify_meeting_link_sent_to_participants
from .eval_11 import verify_scheduled_meeting_canceled
from .eval_12 import TASK12_ANSWER_SCHEMA, verify_not_started_meeting_count_and_invite_link
from .eval_13 import verify_contact_message_sent_and_recent_chat
from .eval_14 import TASK14_ANSWER_SCHEMA, verify_unread_chat_thread_count_after_messages
from .eval_15 import verify_meeting_media_defaults_updated
from .eval_16 import verify_personal_meeting_link_sent_and_returned
from .eval_17 import TASK17_ANSWER_SCHEMA, verify_upcoming_meeting_count_and_rename
from .eval_18 import verify_nearest_upcoming_meeting_waiting_room_enabled
from .eval_19 import verify_personal_status_busy
from .eval_20 import verify_display_name_updated

ZOOM_TASKS = AppTasks(
    package_name="com.example.zoom",
    task_items=[
        TaskItem(
            instruction='Create an instant meeting named "[GUIA-02] Instant Sync", invite Amber Campbell and Brittany Evans, enable the waiting room, disable "Allow participants to join before host", copy the meeting number and invite link, then end the meeting.',
            verify_func=verify_instant_meeting_invite_and_settings,
            human_steps=18,
        ),
        TaskItem(
            instruction="Join meeting 994488281; if your local microphone is on, turn it off and keep only the camera on; after joining, send \"I'm lcl.\", raise your hand and then lower it, reply with a thumbs-up emoji, and then leave the meeting.",
            verify_func=verify_meeting_participation_and_chat_actions,
            human_steps=14,
        ),
        TaskItem(
            instruction='Join meeting 389257198, open the participant list, mute all participants first, then unmute Amber Campbell, send "Amber, please start." in chat, and lock the meeting.',
            verify_func=verify_meeting_participant_controls_and_lock,
            human_steps=14,
        ),
        TaskItem(
            instruction='Create an instant meeting and start screen sharing. After pausing sharing, send "Sharing paused." in chat, then resume sharing, stop sharing, and end the meeting.',
            verify_func=verify_screen_sharing_pause_resume_and_chat,
            human_steps=16,
        ),
        TaskItem(
            instruction='Create an instant meeting, turn on the microphone and camera first, then disconnect audio, send "Audio disconnected, video on." in chat, and end the meeting.',
            verify_func=verify_meeting_media_state_and_chat,
            human_steps=10,
        ),
        TaskItem(
            instruction='Schedule a meeting for tomorrow from 19:00 to 20:30 with the title "[GUIA-07] Project Sync", invite Derek Stewart and Brittany Evans, enable the waiting room and password, turn on host video and turn off participant video, save it, and return to the meeting list.',
            verify_func=verify_scheduled_meeting_created_with_invite_settings,
            human_steps=17,
        ),
        TaskItem(
            instruction='Schedule a recurring meeting for the day after tomorrow from 09:30 to 10:00 with the title "[GUIA-08] Daily Standup", set it to repeat every weekday, invite Amber Campbell and Natalie Cox, disable "Allow participants to join before host", and save.',
            verify_func=verify_recurring_meeting_created_with_participants,
            human_steps=14,
        ),
        TaskItem(
            instruction='Find the meeting titled "[GUIA-07] Project Sync", change the start time to tomorrow at 19:30, change the duration to 2 hours, add Natalie Cox as a participant, and enable the waiting room.',
            verify_func=verify_scheduled_meeting_updated_with_participant_and_waiting_room,
            human_steps=17,
        ),
        TaskItem(
            instruction='Find the scheduled meeting at 12:00 tomorrow, move it to 13:00 and extend the duration to 4 hours.',
            verify_func=verify_scheduled_meeting_time_and_duration_updated,
            human_steps=8,
        ),
        TaskItem(
            instruction='Open the scheduled meeting at 08:00 tomorrow, copy the invite link, then send Derek Stewart and Brittany Evans the message "The meeting link has been updated. Please check." and paste the link.',
            verify_func=verify_meeting_link_sent_to_participants,
            human_steps=14,
        ),
        TaskItem(
            instruction='Cancel the earliest scheduled meeting whose title contains "[GUIA]" and whose date is May 1, then return to the list and confirm it no longer exists.',
            verify_func=verify_scheduled_meeting_canceled,
            human_steps=2,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction='Count all currently "Not started" scheduled meetings, then open the earliest one, copy its invite link, and return to the meeting list.',
            verify_func=verify_not_started_meeting_count_and_invite_link,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="hybrid",
            answer_schema=TASK12_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Search for Natalie Cox in the contacts list, send the message \"I need to take leave from next Monday's meeting.\", return to the chat list, and confirm this conversation appears in recent chats.",
            verify_func=verify_contact_message_sent_and_recent_chat,
            human_steps=8,
        ),
        TaskItem(
            instruction="Find Amber Campbell and Derek Stewart in the contacts list, send each of them \"Please confirm tomorrow's meeting.\", then count the current number of unread chat threads.",
            verify_func=verify_unread_chat_thread_count_after_messages,
            human_steps=13,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="hybrid",
            answer_schema=TASK14_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Open Settings, turn off "Automatically connect audio when joining meeting", turn on "Always turn on camera when joining meeting", then immediately create a meeting and confirm the camera is on while audio is disconnected.',
            verify_func=verify_meeting_media_defaults_updated,
            human_steps=10,
        ),
        TaskItem(
            instruction='Start a meeting using your Personal Meeting ID, copy the invite link, send Amber Campbell the message "Please use this link to join the meeting:" and paste the link, then return to the meeting.',
            verify_func=verify_personal_meeting_link_sent_and_returned,
            human_steps=15,
        ),
        TaskItem(
            instruction='Find all not-started meetings in the next 7 days, count them, and rename the latest-starting one to "[GUIA-19] Final Review".',
            verify_func=verify_upcoming_meeting_count_and_rename,
            human_steps=5,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COUNT,
                NumericReasoningCategory.COMPARE_SELECT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="hybrid",
            answer_schema=TASK17_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Find the nearest scheduled meeting that has not started yet, enable the waiting room, disable "Allow participants to join before host", save it, and return to the meeting list.',
            verify_func=verify_nearest_upcoming_meeting_waiting_room_enabled,
            human_steps=6,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction='Change my personal status to "Busy".',
            verify_func=verify_personal_status_busy,
            human_steps=5,
        ),
        TaskItem(
            instruction='Change my display name to "Liu Chenlong".',
            verify_func=verify_display_name_updated,
            human_steps=5,
        ),
    ],
)
