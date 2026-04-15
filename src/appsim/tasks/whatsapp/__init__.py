from ..base import AppTasks, TaskItem
from .eval_1 import validate_task_one
from .eval_2 import validate_task_two
from .eval_3 import validate_task_three
from .eval_4 import validate_task_four
from .eval_5 import validate_task_five
from .eval_6 import validate_task_six
from .eval_7 import validate_task_seven
from .eval_8 import validate_task_eight
from .eval_9 import validate_task_nine
from .eval_10 import validate_task_ten
from .eval_11 import validate_task_eleven
from .eval_12 import validate_task_twelve
from .eval_13 import validate_task_thirteen
from .eval_14 import validate_task_fourteen
from .eval_15 import validate_task_fifteen
from .eval_16 import validate_task_sixteen
from .eval_17 import validate_task_seventeen
from .eval_18 import validate_task_eighteen
from .eval_19 import validate_task_nineteen
from .eval_20 import validate_task_twenty
from .eval_21 import validate_task_twenty_one
from .eval_22 import validate_task_twenty_two
from .eval_23 import validate_task_twenty_three
from .eval_24 import validate_task_twenty_four
from .eval_25 import validate_task_twenty_five
from .eval_26 import validate_task_twenty_six
from .eval_27 import validate_task_twenty_seven
from .eval_28 import validate_task_twenty_eight
from .eval_29 import validate_task_twenty_nine
from .eval_30 import validate_task_thirty
from .eval_31 import validate_task_thirty_one
from .eval_32 import validate_task_thirty_two
from .eval_33 import validate_task_thirty_three
from .eval_34 import validate_task_thirty_four
from .eval_35 import validate_task_thirty_five
from .eval_36 import validate_task_thirty_six
from .eval_37 import validate_task_thirty_seven
from .eval_38 import validate_task_thirty_eight
from .eval_39 import validate_task_thirty_nine
from .eval_40 import validate_task_forty

WHATSAPP_TASKS = AppTasks(
    package_name="com.example.whatsapp_sim",
    task_items=[
        TaskItem(
            instruction="Open the first conversation in the chat list, check who sent the latest message, and tell me the name only.",
            verify_func=validate_task_one,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Tell me who the most recent call was with. Just give me the name.",
            verify_func=validate_task_two,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check the phone number linked to my account and tell me the answer only.",
            verify_func=validate_task_three,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Like Olivia's newly uploaded status.",
            verify_func=validate_task_four,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Send a message to the "Friday Night Plans" group chat saying "I feel so excited!!!".',
            verify_func=validate_task_five,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Tell me who the most recent video call was with. Just give me the name.",
            verify_func=validate_task_six,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Follow the Netflix channel.",
            verify_func=validate_task_seven,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check how many conversations have unread messages and give me an Arabic numeral only.",
            verify_func=validate_task_eight,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how many communities I have joined.",
            verify_func=validate_task_nine,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how many statuses the Spotify channel has posted in total and give me an Arabic numeral only.",
            verify_func=validate_task_ten,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Create a new conversation with James Walker and tell him "We should have a meeting at 2pm".',
            verify_func=validate_task_eleven,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Change my personal status to Busy.",
            verify_func=validate_task_twelve,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Post a status on the Updates page with a yellow background and the content "Sunshine".',
            verify_func=validate_task_thirteen,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Open the chat list, find the first group chat with unread messages, enter it, and reply "OK".',
            verify_func=validate_task_fourteen,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add Isabella Martinez to the Startup Ideas group chat.",
            verify_func=validate_task_fifteen,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Forward the most commented status from the Netflix channel to Emily Chen.",
            verify_func=validate_task_sixteen,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Create a new contact named Jaye Zhang with the phone number (415) 555-1230.",
            verify_func=validate_task_seventeen,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Start a call with Ethan Garcia and Lucas Anderson, then hang up.",
            verify_func=validate_task_eighteen,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Mute notifications for the first conversation in the chat list, then return to the list and confirm that the mute icon is shown.",
            verify_func=validate_task_nineteen,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Go to the Calls page and send a text message saying "Hello, are you free?" to the first contact in the call log.',
            verify_func=validate_task_twenty,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Find the status about Taylor Swift in the Spotify channel and react with a fire emoji.",
            verify_func=validate_task_twenty_one,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Mute the channel with the most followers on the Updates page.",
            verify_func=validate_task_twenty_two,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add Mia Harris and Noah Kim to the NYC Foodies community.",
            verify_func=validate_task_twenty_three,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Start a video call in the Weekend Hiking Crew group chat, keep it going for more than 5 seconds, then hang up.",
            verify_func=validate_task_twenty_four,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Create a new community named "Hip-hop music enthusiasts" with the description "Welcome all hip-hop music enthusiasts to join this community. Please share and discuss your favorite music!"',
            verify_func=validate_task_twenty_five,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Create a new group chat with Rachel Green, Sophia Lee, and Tom Briggs, set the group name to "Project Discussion Group", then enter the chat and send the message "Hello everyone, welcome to join the project discussion group!".',
            verify_func=validate_task_twenty_six,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Create a new community named "Book Club" and add the first two contacts.',
            verify_func=validate_task_twenty_seven,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check the latest message Noah Kim sent me, read what he asked me to do, and do as he said.",
            verify_func=validate_task_twenty_eight,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='From the chat list, open the third group chat, view the member list, find the group admin\'s name, and send that admin a private message saying "Hello, I\'m a member of the group. I have a question to ask.".',
            verify_func=validate_task_twenty_nine,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Find the status in the Spotify channel about this week\'s hottest playlist, forward it to the Weekend Hiking Crew group chat, and ask everyone "Which song do you pick?"',
            verify_func=validate_task_thirty,
            human_steps=15,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Create a new broadcast list with Ava, Emily Chen, Ethan Garcia, and Isabella Martinez, then send the message "Please submit this week\'s report by Friday. Make sure to complete it on time.".',
            verify_func=validate_task_thirty_one,
            human_steps=13,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Open the channel where Marcus Davis shared his status, send a red heart reaction to that status, then return to the chat and send him "Thanks for sharing!"',
            verify_func=validate_task_thirty_two,
            human_steps=13,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Mute the first three group chat conversations in order.",
            verify_func=validate_task_thirty_three,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Find the contact who appears most often in the call log, open the conversation with them from the chat list, and send the message "Feel free to contact me at any time.".',
            verify_func=validate_task_thirty_four,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Enter the first community, check and note the latest announcement, then go to that community\'s General chat and send the message "Tip: [announcement content]" with the actual announcement content filled in.',
            verify_func=validate_task_thirty_five,
            human_steps=16,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Send "ok" to every conversation with more than 3 unread messages.',
            verify_func=validate_task_thirty_six,
            human_steps=13,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add a new contact Jessie Brown with the phone number (415) 555-1013, then add her to the SF Tech Squad group chat.",
            verify_func=validate_task_thirty_seven,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="React to every friend's status with a purple heart.",
            verify_func=validate_task_thirty_eight,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Start a call with all contacts whose names start with L, switch it to a video call, keep it going for 10 seconds, then hang up.",
            verify_func=validate_task_thirty_nine,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Go to the Netflix channel, find the release date of Black Mirror S7, and tell Sophia Lee the information.",
            verify_func=validate_task_forty,
            human_steps=14,
            is_reasoning=True,
        ),
    ],
)
