from ..base import AppTasks, TaskItem

from .eval_1 import TASK1_ANSWER_SCHEMA, verify_nearby_restaurant_exists
from .eval_2 import verify_food_item_purchased
from .eval_3 import verify_home_address_created
from .eval_4 import verify_cart_purchased
from .eval_5 import verify_live_location_enabled
from .eval_6 import verify_cheapest_ride_booked
from .eval_7 import TASK7_ANSWER_SCHEMA, verify_nearby_pickup_location_exists
from .eval_8 import verify_scheduled_multi_item_order_created
from .eval_9 import verify_hearing_assistance_enabled
from .eval_10 import TASK10_ANSWER_SCHEMA, verify_cheapest_nearby_menu_item
from .eval_11 import TASK11_ANSWER_SCHEMA, verify_cart_total_price
from .eval_12 import TASK12_ANSWER_SCHEMA, verify_food_delivery_spending_before_date
from .eval_13 import TASK13_ANSWER_SCHEMA, verify_free_delivery_merchant_count
from .eval_14 import TASK14_ANSWER_SCHEMA, verify_account_balance
from .eval_15 import TASK15_ANSWER_SCHEMA, verify_past_category_merchant_count
from .eval_16 import TASK16_ANSWER_SCHEMA, verify_latest_order_arrival_time
from .eval_17 import TASK17_ANSWER_SCHEMA, verify_category_delivery_spending_between_dates
from .eval_18 import TASK18_ANSWER_SCHEMA, verify_beverage_spending_since_date
from .eval_19 import TASK19_ANSWER_SCHEMA, verify_app_version
from .eval_20 import TASK20_ANSWER_SCHEMA, verify_cheapest_homepage_burger
from .eval_21 import TASK21_ANSWER_SCHEMA, verify_cheapest_item_price_difference_between_merchants
from .eval_22 import verify_multiple_restaurant_items_added_to_cart
from .eval_23 import verify_scheduled_multi_merchant_order_created
from .eval_24 import TASK24_ANSWER_SCHEMA, verify_preferred_food_category
from .eval_25 import verify_burger_merchants_favorited
from .eval_26 import TASK26_ANSWER_SCHEMA, verify_past_burger_spending
from .eval_27 import TASK27_ANSWER_SCHEMA, verify_past_pizza_spending
from .eval_28 import TASK28_ANSWER_SCHEMA, verify_past_beverage_spending
from .eval_29 import TASK29_ANSWER_SCHEMA, verify_past_matcha_spending
from .eval_30 import verify_courier_message_sent
from .eval_31 import verify_scheduled_multi_item_order_created_with_extra_items
from .eval_32 import verify_multi_merchant_food_order_created
from .eval_33 import verify_food_order_and_ride_booked
from .eval_34 import verify_work_and_home_addresses_created

UBEREATS_TASKS = AppTasks(
    package_name="com.example.ubereats_sim",
    task_items=[
        TaskItem(
            instruction="I want to eat McDonald's. Search for McDonald's and see whether there is one nearby, then respond with yes or no.",
            verify_func=verify_nearby_restaurant_exists,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Help me buy one McDonald's Hash Browns, with default delivery info.",
            verify_func=verify_food_item_purchased,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add a new house entry with the location set to jianghanlu.",
            verify_func=verify_home_address_created,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Buy all items in the cart, with default delivery info.",
            verify_func=verify_cart_purchased,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Turn on the livelocation option.",
            verify_func=verify_live_location_enabled,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Book a ride from jianghanlu to jiedaokou and choose the cheapest ride type.",
            verify_func=verify_cheapest_ride_booked,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="I want to eat at McDonald's in store. Search whether there is a pickup point nearby, then respond with yes or no.",
            verify_func=verify_nearby_pickup_location_exists,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK7_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Help me order McDonald's Hash Browns and Double Cheeseburger, choose tomorrow at 12 PM, and keep all other delivery info as default.",
            verify_func=verify_scheduled_multi_item_order_created,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Turn on the hard of hearing option in hearing.",
            verify_func=verify_hearing_assistance_enabled,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check what the cheapest item at a nearby McDonald's is.",
            verify_func=verify_cheapest_nearby_menu_item,
            human_steps=7,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK10_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="How much would it cost to buy everything currently in the cart?",
            verify_func=verify_cart_total_price,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK11_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how much I spent on food delivery before 3.29.",
            verify_func=verify_food_delivery_spending_before_date,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK12_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Among the first eight merchants on the home page, how many have free delivery?",
            verify_func=verify_free_delivery_merchant_count,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK13_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how much money is left in my Uber account.",
            verify_func=verify_account_balance,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK14_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Among the merchants I ordered from before, how many sell burgers or pizza?",
            verify_func=verify_past_category_merchant_count,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK15_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check when my latest order is expected to arrive.",
            verify_func=verify_latest_order_arrival_time,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK16_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how much I spent at burger or pizza places from 3.17 to 3.22.",
            verify_func=verify_category_delivery_spending_between_dates,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK17_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Calculate how much I have spent on drinks since 3.17.",
            verify_func=verify_beverage_spending_since_date,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="It feels like a feature is missing. What is the current app version?",
            verify_func=verify_app_version,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK19_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="On the home page McDonald's, which burger is the cheapest?",
            verify_func=verify_cheapest_homepage_burger,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK20_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="How much is the cheapest item at Matchaful on the home page cheaper than the cheapest item at HAWA SMOOTHIES? I am very poor right now.",
            verify_func=verify_cheapest_item_price_difference_between_merchants,
            human_steps=16,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK21_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Add McDonald's Hash Brown and Double Cheeseburger to the cart, then add Burger King's Whopper to the cart.",
            verify_func=verify_multiple_restaurant_items_added_to_cart,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Help me order a lunch to be delivered tomorrow at 12 PM. I want HAWA SMOOTHIES's Mango Pineapple Smoothie and a 7-Eleven Turkey Sandwich.",
            verify_func=verify_scheduled_multi_merchant_order_created,
            human_steps=27,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Look at my past purchases. Do I prefer Burger or Pizza?",
            verify_func=verify_preferred_food_category,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK24_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Add to favorites the stores among the first eight shown on the home page that sell burgers.",
            verify_func=verify_burger_merchants_favorited,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Calculate how much I spent on burgers in past purchases, excluding delivery fees.",
            verify_func=verify_past_burger_spending,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK26_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how much I spent on pizza in past purchases, excluding delivery fees.",
            verify_func=verify_past_pizza_spending,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK27_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how much I spent on drinks in past purchases.",
            verify_func=verify_past_beverage_spending,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK28_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how much I spent on matcha items in past purchases.",
            verify_func=verify_past_matcha_spending,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK29_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Send a message to the courier of my latest order asking \"How long will it take to arrive?\"",
            verify_func=verify_courier_message_sent,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Help me order a lunch to be delivered tomorrow at 12 PM. I want HAWA SMOOTHIES's Mango Pineapple Smoothie, Burger King's Onion Rings, and Bacon King.",
            verify_func=verify_scheduled_multi_item_order_created_with_extra_items,
            human_steps=26,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="I want to drink Benvenuto's Espresso and eat Yunnan Rice Noodle's Cold Noodle Salad.",
            verify_func=verify_multi_merchant_food_order_created,
            human_steps=21,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="I want to drink Benvenuto's Espresso and eat Yunnan Rice Noodle's Cold Noodle Salad, then book a ride from jiedaokou to jianghanlu with any ride type.",
            verify_func=verify_food_order_and_ride_booked,
            human_steps=27,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add a work office address as jiedaokou, and add a home house address as jianghanlu.",
            verify_func=verify_work_and_home_addresses_created,
            human_steps=13,
            is_reasoning=False,
        ),
    ],
)
