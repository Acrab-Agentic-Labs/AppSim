# All instructions: file index equals task index
# type: ignore
# noqa
from ..base import AppTasks, TaskItem


from .eval_1 import verify_invite_amber_to_new_meeting
from .eval_2 import verify_copy_invite_link_then_leave
from .eval_3 import verify_screen_share_in_new_meeting
from .eval_4 import verify_safe_driving_hello
from .eval_5 import verify_media_enabled_before_host
from .eval_6 import verify_send_im_lcl_in_new_meeting
from .eval_7 import verify_busy_status
from .eval_8 import verify_display_name_updated
from .eval_9 import verify_join_994488281_with_camera
from .eval_10 import verify_unmute_all_389257198
from .eval_11 import verify_raise_lower_hand_with_thumbs_up
from .eval_12 import verify_contact_count_answer
from .eval_13 import verify_upcoming_schedule_count_answer
from .eval_14 import verify_schedule_tomorrow_1900_with_derek_and_brittany
from .eval_15 import verify_cancel_may_first_schedule
from .eval_16 import verify_message_natalie_about_next_monday_leave
from .eval_17 import verify_delay_tomorrow_noon_to_1300
from .eval_18 import verify_enable_waiting_room_and_extend_noon_meeting
from .eval_19 import verify_change_personal_status_to_busy
from .eval_20 import verify_change_display_name_to_liu_chenlong

ZOOM_TASKS = AppTasks(
    package_name="com.example.zoom",
    task_items=[
        TaskItem(
            instruction='Create an instant meeting named "[GUIA-02] Instant Sync", invite Amber Campbell and Brittany Evans, enable the waiting room, disable "Allow participants to join before host", copy the meeting number and invite link, then end the meeting.',
            verify_func=verify_invite_amber_to_new_meeting,
            human_steps=18,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Join meeting 994488281; if your local microphone is on, turn it off and keep only the camera on; after joining, send \"I'm lcl.\", raise your hand and then lower it, reply with a thumbs-up emoji, and then leave the meeting.",
            verify_func=verify_copy_invite_link_then_leave,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Join meeting 389257198, open the participant list, mute all participants first, then unmute Amber Campbell, send "Amber, please start." in chat, and lock the meeting.',
            verify_func=verify_screen_share_in_new_meeting,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Create an instant meeting and start screen sharing. After pausing sharing, send "Sharing paused." in chat, then resume sharing, stop sharing, and end the meeting.',
            verify_func=verify_safe_driving_hello,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Create an instant meeting, turn on the microphone and camera first, then disconnect audio, send "Audio disconnected, video on." in chat, and end the meeting.',
            verify_func=verify_media_enabled_before_host,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Schedule a meeting for tomorrow from 19:00 to 20:30 with the title "[GUIA-07] Project Sync", invite Derek Stewart and Brittany Evans, enable the waiting room and password, turn on host video and turn off participant video, save it, and return to the meeting list.',
            verify_func=verify_send_im_lcl_in_new_meeting,
            human_steps=17,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Schedule a recurring meeting for the day after tomorrow from 09:30 to 10:00 with the title "[GUIA-08] Daily Standup", set it to repeat every weekday, invite Amber Campbell and Natalie Cox, disable "Allow participants to join before host", and save.',
            verify_func=verify_busy_status,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Find the meeting titled "[GUIA-07] Project Sync", change the start time to tomorrow at 19:30, change the duration to 2 hours, add Natalie Cox as a participant, and enable the waiting room.',
            verify_func=verify_display_name_updated,
            human_steps=17,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Find the scheduled meeting at 12:00 tomorrow, move it to 13:00 and extend the duration to 4 hours.',
            verify_func=verify_join_994488281_with_camera,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Open the scheduled meeting at 08:00 tomorrow, copy the invite link, then send Derek Stewart and Brittany Evans the message "The meeting link has been updated. Please check." and paste the link.',
            verify_func=verify_unmute_all_389257198,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Cancel the earliest scheduled meeting whose title contains "[GUIA]" and whose date is May 1, then return to the list and confirm it no longer exists.',
            verify_func=verify_raise_lower_hand_with_thumbs_up,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Count all currently "Not started" scheduled meetings, then open the earliest one, copy its invite link, and return to the meeting list. Put the numeric answer between <ans> and </ans>, using Arabic numerals, for example <ans>3</ans>.',
            verify_func=verify_contact_count_answer,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Search for Natalie Cox in the contacts list, send the message \"I need to take leave from next Monday's meeting.\", return to the chat list, and confirm this conversation appears in recent chats.",
            verify_func=verify_upcoming_schedule_count_answer,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Find Amber Campbell and Derek Stewart in the contacts list, send each of them \"Please confirm tomorrow's meeting.\", then count the current number of unread chat threads. Put the numeric answer between <ans> and </ans>, using Arabic numerals, for example <ans>3</ans>.",
            verify_func=verify_schedule_tomorrow_1900_with_derek_and_brittany,
            human_steps=13,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Open Settings, turn off "Automatically connect audio when joining meeting", turn on "Always turn on camera when joining meeting", then immediately create a meeting and confirm the camera is on while audio is disconnected.',
            verify_func=verify_cancel_may_first_schedule,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Start a meeting using your Personal Meeting ID, copy the invite link, send Amber Campbell the message "Please use this link to join the meeting:" and paste the link, then return to the meeting.',
            verify_func=verify_message_natalie_about_next_monday_leave,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Find all not-started meetings in the next 7 days, count them, and rename the latest-starting one to "[GUIA-19] Final Review". Put the numeric answer between <ans> and </ans>, using Arabic numerals, for example <ans>3</ans>.',
            verify_func=verify_delay_tomorrow_noon_to_1300,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Find the nearest scheduled meeting that has not started yet, enable the waiting room, disable "Allow participants to join before host", save it, and return to the meeting list.',
            verify_func=verify_enable_waiting_room_and_extend_noon_meeting,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Change my personal status to "Busy".',
            verify_func=verify_change_personal_status_to_busy,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Change my display name to "Liu Chenlong".',
            verify_func=verify_change_display_name_to_liu_chenlong,
            human_steps=5,
            is_reasoning=False,
        ),
    ],
)
