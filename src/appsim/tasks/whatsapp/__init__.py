from ..base import AppTasks, NumericReasoningCategory, TaskItem
from .eval_1 import verify_latest_chat_sender_identified, TASK1_ANSWER_SCHEMA
from .eval_2 import verify_latest_call_contact_identified, TASK2_ANSWER_SCHEMA
from .eval_3 import TASK3_ANSWER_SCHEMA, verify_account_phone_number_retrieved
from .eval_4 import verify_friend_status_liked
from .eval_5 import verify_group_message_sent
from .eval_6 import verify_latest_video_call_contact_identified, TASK6_ANSWER_SCHEMA
from .eval_7 import verify_channel_followed
from .eval_8 import TASK8_ANSWER_SCHEMA, verify_unread_chat_count
from .eval_9 import TASK9_ANSWER_SCHEMA, verify_joined_community_count
from .eval_10 import TASK10_ANSWER_SCHEMA, verify_channel_status_count
from .eval_11 import verify_new_conversation_message_sent
from .eval_12 import verify_personal_status_updated
from .eval_13 import verify_status_posted_with_background
from .eval_14 import verify_unread_group_message_replied
from .eval_15 import verify_group_participant_added
from .eval_16 import verify_most_commented_status_forwarded
from .eval_17 import verify_contact_created
from .eval_18 import verify_group_call_completed
from .eval_19 import verify_chat_notifications_muted
from .eval_20 import verify_call_log_contact_messaged
from .eval_21 import verify_status_reaction_added
from .eval_22 import verify_top_followed_channel_muted
from .eval_23 import verify_community_participants_added
from .eval_24 import verify_group_video_call_completed
from .eval_25 import verify_community_created_with_description
from .eval_26 import verify_group_created_and_message_sent
from .eval_27 import verify_community_created_with_contacts
from .eval_28 import verify_latest_incoming_message_request_completed
from .eval_29 import verify_group_admin_messaged
from .eval_30 import verify_status_forwarded_and_group_message_sent
from .eval_31 import verify_broadcast_list_created_and_message_sent
from .eval_32 import verify_status_reacted_to_and_contact_messaged
from .eval_33 import verify_multiple_group_chats_muted
from .eval_34 import verify_most_frequent_call_contact_messaged
from .eval_35 import verify_community_announcement_shared
from .eval_36 import verify_high_unread_chats_replied_to
from .eval_37 import verify_contact_created_and_group_added
from .eval_38 import verify_friend_statuses_reacted_to
from .eval_39 import verify_multiple_contacts_video_called
from .eval_40 import verify_channel_information_shared

WHATSAPP_TASKS = AppTasks(
    package_name="com.example.whatsapp_sim",
    task_items=[
        TaskItem(
            instruction="Open the first conversation in the chat list, check who sent the latest message, and tell me the name only.",
            verify_func=verify_latest_chat_sender_identified,
            human_steps=3,
            evaluation_type="answer",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Tell me who the most recent call was with. Just give me the name.",
            verify_func=verify_latest_call_contact_identified,
            human_steps=3,
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check the phone number linked to my account and tell me the answer only.",
            verify_func=verify_account_phone_number_retrieved,
            human_steps=3,
            evaluation_type="answer",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Like Olivia's newly uploaded status.",
            verify_func=verify_friend_status_liked,
            human_steps=4,
        ),
        TaskItem(
            instruction='Send a message to the "Friday Night Plans" group chat saying "I feel so excited!!!".',
            verify_func=verify_group_message_sent,
            human_steps=4,
        ),
        TaskItem(
            instruction="Tell me who the most recent video call was with. Just give me the name.",
            verify_func=verify_latest_video_call_contact_identified,
            human_steps=4,
            evaluation_type="answer",
            answer_schema=TASK6_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Follow the Netflix channel.",
            verify_func=verify_channel_followed,
            human_steps=3,
        ),
        TaskItem(
            instruction="Check how many conversations have unread messages and give me an Arabic numeral only.",
            verify_func=verify_unread_chat_count,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK8_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how many communities I have joined.",
            verify_func=verify_joined_community_count,
            human_steps=2,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK9_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how many statuses the Spotify channel has posted in total and give me an Arabic numeral only.",
            verify_func=verify_channel_status_count,
            human_steps=5,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK10_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Create a new conversation with James Walker and tell him "We should have a meeting at 2pm".',
            verify_func=verify_new_conversation_message_sent,
            human_steps=8,
        ),
        TaskItem(
            instruction="Change my personal status to Busy.",
            verify_func=verify_personal_status_updated,
            human_steps=6,
        ),
        TaskItem(
            instruction='Post a status on the Updates page with a yellow background and the content "Sunshine".',
            verify_func=verify_status_posted_with_background,
            human_steps=7,
        ),
        TaskItem(
            instruction='Open the chat list, find the first group chat with unread messages, enter it, and reply "OK".',
            verify_func=verify_unread_group_message_replied,
            human_steps=6,
        ),
        TaskItem(
            instruction="Add Isabella Martinez to the Startup Ideas group chat.",
            verify_func=verify_group_participant_added,
            human_steps=7,
        ),
        TaskItem(
            instruction="Forward the most commented status from the Netflix channel to Emily Chen.",
            verify_func=verify_most_commented_status_forwarded,
            human_steps=8,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="Create a new contact named Jaye Zhang with the phone number (415) 555-1230.",
            verify_func=verify_contact_created,
            human_steps=8,
        ),
        TaskItem(
            instruction="Start a call with Ethan Garcia and Lucas Anderson, then hang up.",
            verify_func=verify_group_call_completed,
            human_steps=8,
        ),
        TaskItem(
            instruction="Mute notifications for the first conversation in the chat list, then return to the list and confirm that the mute icon is shown.",
            verify_func=verify_chat_notifications_muted,
            human_steps=7,
        ),
        TaskItem(
            instruction='Go to the Calls page and send a text message saying "Hello, are you free?" to the first contact in the call log.',
            verify_func=verify_call_log_contact_messaged,
            human_steps=8,
        ),
        TaskItem(
            instruction="Find the status about Taylor Swift in the Spotify channel and react with a fire emoji.",
            verify_func=verify_status_reaction_added,
            human_steps=6,
        ),
        TaskItem(
            instruction="Mute the channel with the most followers on the Updates page.",
            verify_func=verify_top_followed_channel_muted,
            human_steps=6,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="Add Mia Harris and Noah Kim to the NYC Foodies community.",
            verify_func=verify_community_participants_added,
            human_steps=7,
        ),
        TaskItem(
            instruction="Start a video call in the Weekend Hiking Crew group chat, keep it going for more than 5 seconds, then hang up.",
            verify_func=verify_group_video_call_completed,
            human_steps=6,
        ),
        TaskItem(
            instruction='Create a new community named "Hip-hop music enthusiasts" with the description "Welcome all hip-hop music enthusiasts to join this community. Please share and discuss your favorite music!"',
            verify_func=verify_community_created_with_description,
            human_steps=8,
        ),
        TaskItem(
            instruction='Create a new group chat with Rachel Green, Sophia Lee, and Tom Briggs, set the group name to "Project Discussion Group", then enter the chat and send the message "Hello everyone, welcome to join the project discussion group!".',
            verify_func=verify_group_created_and_message_sent,
            human_steps=14,
        ),
        TaskItem(
            instruction='Create a new community named "Book Club" and add the first two contacts.',
            verify_func=verify_community_created_with_contacts,
            human_steps=11,
        ),
        TaskItem(
            instruction="Check the latest message Noah Kim sent me, read what he asked me to do, and do as he said.",
            verify_func=verify_latest_incoming_message_request_completed,
            human_steps=12,
        ),
        TaskItem(
            instruction='From the chat list, open the third group chat, view the member list, find the group admin\'s name, and send that admin a private message saying "Hello, I\'m a member of the group. I have a question to ask.".',
            verify_func=verify_group_admin_messaged,
            human_steps=12,
        ),
        TaskItem(
            instruction='Find the status in the Spotify channel about this week\'s hottest playlist, forward it to the Weekend Hiking Crew group chat, and ask everyone "Which song do you pick?"',
            verify_func=verify_status_forwarded_and_group_message_sent,
            human_steps=15,
        ),
        TaskItem(
            instruction='Create a new broadcast list with Ava, Emily Chen, Ethan Garcia, and Isabella Martinez, then send the message "Please submit this week\'s report by Friday. Make sure to complete it on time.".',
            verify_func=verify_broadcast_list_created_and_message_sent,
            human_steps=13,
        ),
        TaskItem(
            instruction='Open the channel where Marcus Davis shared his status, send a red heart reaction to that status, then return to the chat and send him "Thanks for sharing!"',
            verify_func=verify_status_reacted_to_and_contact_messaged,
            human_steps=13,
        ),
        TaskItem(
            instruction="Mute the first three group chat conversations in order.",
            verify_func=verify_multiple_group_chats_muted,
            human_steps=14,
        ),
        TaskItem(
            instruction='Find the contact who appears most often in the call log, open the conversation with them from the chat list, and send the message "Feel free to contact me at any time.".',
            verify_func=verify_most_frequent_call_contact_messaged,
            human_steps=12,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction='Enter the first community, check and note the latest announcement, then go to that community\'s General chat and send the message "Tip: [announcement content]" with the actual announcement content filled in.',
            verify_func=verify_community_announcement_shared,
            human_steps=16,
        ),
        TaskItem(
            instruction='Send "ok" to every conversation with more than 3 unread messages.',
            verify_func=verify_high_unread_chats_replied_to,
            human_steps=13,
            numeric_reasoning_categories=[NumericReasoningCategory.THRESHOLD_FILTER],
        ),
        TaskItem(
            instruction="Add a new contact Jessie Brown with the phone number (415) 555-1013, then add her to the SF Tech Squad group chat.",
            verify_func=verify_contact_created_and_group_added,
            human_steps=12,
        ),
        TaskItem(
            instruction="React to every friend's status with a purple heart.",
            verify_func=verify_friend_statuses_reacted_to,
            human_steps=13,
        ),
        TaskItem(
            instruction="Start a call with all contacts whose names start with L, switch it to a video call, keep it going for 10 seconds, then hang up.",
            verify_func=verify_multiple_contacts_video_called,
            human_steps=12,
        ),
        TaskItem(
            instruction="Go to the Netflix channel, find the release date of Black Mirror S7, and tell Sophia Lee the information.",
            verify_func=verify_channel_information_shared,
            human_steps=14,
        ),
    ],
)
