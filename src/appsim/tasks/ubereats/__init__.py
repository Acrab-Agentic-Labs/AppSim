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


UBEREATS_TASKS = AppTasks(
    package_name="com.example.ubereats_sim",
    task_items=[
        TaskItem(
            instruction="I want to eat McDonald's. Search for McDonald's and see whether there is one nearby, then respond with yes or no.",
            verify_func=validate_task_one,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Help me buy one McDonald's Hash Browns, with default delivery info.",
            verify_func=validate_task_two,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add a new house entry with the location set to jianghanlu.",
            verify_func=validate_task_three,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Buy all items in the cart, with default delivery info.",
            verify_func=validate_task_four,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Turn on the livelocation option.",
            verify_func=validate_task_five,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Book a ride from jianghanlu to jiedaokou and choose the cheapest ride type.",
            verify_func=validate_task_six,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="I want to eat at McDonald's in store. Search whether there is a pickup point nearby, then respond with yes or no.",
            verify_func=validate_task_seven,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Help me order McDonald's Hash Browns and Double Cheeseburger, choose tomorrow at 12 PM, and keep all other delivery info as default.",
            verify_func=validate_task_eight,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Turn on the hard of hearing option in hearing.",
            verify_func=validate_task_nine,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check what the cheapest item at a nearby McDonald's is.",
            verify_func=validate_task_ten,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="How much would it cost to buy everything currently in the cart?",
            verify_func=validate_task_eleven,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how much I spent on food delivery before 3.29.",
            verify_func=validate_task_twelve,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Among the first eight merchants on the home page, how many have free delivery?",
            verify_func=validate_task_thirteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how much money is left in my Uber account.",
            verify_func=validate_task_fourteen,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Among the merchants I ordered from before, how many sell burgers or pizza?",
            verify_func=validate_task_fifteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check when my latest order is expected to arrive.",
            verify_func=validate_task_sixteen,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how much I spent at burger or pizza places from 3.17 to 3.22.",
            verify_func=validate_task_seventeen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Calculate how much I have spent on drinks since 3.17.",
            verify_func=validate_task_eighteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="It feels like a feature is missing. What is the current app version?",
            verify_func=validate_task_nineteen,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="On the home page McDonald's, which burger is the cheapest?",
            verify_func=validate_task_twenty,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="How much is the cheapest item at Matchaful on the home page cheaper than the cheapest item at HAWA SMOOTHIES? I am very poor right now.",
            verify_func=validate_task_twenty_one,
            human_steps=16,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add McDonald's Hash Brown and Double Cheeseburger to the cart, then add Burger King's Whopper to the cart.",
            verify_func=validate_task_twenty_two,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Help me order a lunch to be delivered tomorrow at 12 PM. I want HAWA SMOOTHIES's Mango Pineapple Smoothie and a 7-Eleven Turkey Sandwich.",
            verify_func=validate_task_twenty_three,
            human_steps=27,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Look at my past purchases. Do I prefer Burger or Pizza?",
            verify_func=validate_task_twenty_four,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add to favorites the stores among the first eight shown on the home page that sell burgers.",
            verify_func=validate_task_twenty_five,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Calculate how much I spent on burgers in past purchases, excluding delivery fees.",
            verify_func=validate_task_twenty_six,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how much I spent on pizza in past purchases, excluding delivery fees.",
            verify_func=validate_task_twenty_seven,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how much I spent on drinks in past purchases.",
            verify_func=validate_task_twenty_eight,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how much I spent on matcha items in past purchases.",
            verify_func=validate_task_twenty_nine,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Send a message to the courier of my latest order asking \"How long will it take to arrive?\"",
            verify_func=validate_task_thirty,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Help me order a lunch to be delivered tomorrow at 12 PM. I want HAWA SMOOTHIES's Mango Pineapple Smoothie, Burger King's Onion Rings, and Bacon King.",
            verify_func=validate_task_thirty_one,
            human_steps=26,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="I want to drink Benvenuto's Espresso and eat Yunnan Rice Noodle's Cold Noodle Salad.",
            verify_func=validate_task_thirty_two,
            human_steps=21,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="I want to drink Benvenuto's Espresso and eat Yunnan Rice Noodle's Cold Noodle Salad, then book a ride from jiedaokou to jianghanlu with any ride type.",
            verify_func=validate_task_thirty_three,
            human_steps=27,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add a work office address as jiedaokou, and add a home house address as jianghanlu.",
            verify_func=validate_task_thirty_four,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Turn on the Live location sharing with couriers option.",
            verify_func=validate_task_thirty_five,
            human_steps=5,
            is_reasoning=False,
        ),
    ],
)
