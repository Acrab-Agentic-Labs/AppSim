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

AMAZON_TASKS = AppTasks(
    package_name="com.example.amazon_sim",
    task_items=[
        TaskItem(
            instruction="Search for 'ball' on the home page, view the search results, and add the first item to the cart.",
            verify_func=validate_task_one,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Calculate the total price of the items in the cart and return only an Arabic numeral.",
            verify_func=validate_task_two,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check how many 'Lifestyle' items are in the Interests section and return only an Arabic numeral.",
            verify_func=validate_task_three,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Send 'Hello' to customer service.",
            verify_func=validate_task_four,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="View my order list, calculate how many orders I have in total, and return only an Arabic numeral.",
            verify_func=validate_task_five,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Select the 12 oz option of Starbucks coffee beans and add it to the cart.",
            verify_func=validate_task_six,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new shopping list named 'My Amazon List'.",
            verify_func=validate_task_seven,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Delete the fourth shipping address.",
            verify_func=validate_task_eight,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Buy a white Nintendo Switch now and check out using Amazon Gift Card.",
            verify_func=validate_task_nine,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Follow the Marshall store.",
            verify_func=validate_task_ten,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Find the highest-rated product in the 'Lifestyle' category and add it to the cart.",
            verify_func=validate_task_eleven,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Buy a watch from the home page right away, choose the lowest-priced option, and have it shipped to Sarah Davis's address.",
            verify_func=validate_task_twelve,
            human_steps=10,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Change the phone number for Robert Taylor's address to '+1(555)613-1230'.",
            verify_func=validate_task_thirteen,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="View the canceled order and tell me its total amount.",
            verify_func=validate_task_fourteen,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Cancel all pending orders.",
            verify_func=validate_task_fifteen,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Buy the items from the first order again.",
            verify_func=validate_task_sixteen,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Remove all items priced below $200 from the cart.",
            verify_func=validate_task_seventeen,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Send 'I want to return my order' to customer service, then check and tell me how many days are mentioned in the reply as the return period. Return only an Arabic numeral.",
            verify_func=validate_task_eighteen,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Search for 'MacBook' and tell me how many reviews mention 'Battery life' in the result item. Return only an Arabic numeral.",
            verify_func=validate_task_nineteen,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Search for 'electronics', count how many items have a rating higher than 4.8, and return only an Arabic numeral.",
            verify_func=validate_task_twenty,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="View the items available for repurchase, find the cheapest one, and add it to the cart.",
            verify_func=validate_task_twenty_one,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="In the cart, find the three most expensive items by unit price, calculate their total price, and return only an Arabic numeral.",
            verify_func=validate_task_twenty_two,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add the item with the most reviews from the list 'Shopping List 2' to the cart.",
            verify_func=validate_task_twenty_three,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check out the most expensive item in the cart.",
            verify_func=validate_task_twenty_four,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Buy the most heavily discounted electronics item on the home page right away.",
            verify_func=validate_task_twenty_five,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Search for 'Dyson', open the first product detail page, add it to the cart, then select it in the cart and check out using Sarah Davis's address.",
            verify_func=validate_task_twenty_six,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add a new shipping address for recipient 'Alex Johnson', phone number '3105550199', address '123 Main St, Apt 8C, Los Angeles, California', ZIP code '90012', and set it as the default address.",
            verify_func=validate_task_twenty_seven,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="On the Interests page, check each of the four categories, calculate the average rating of all products in each category, and give me the highest average rating rounded to two decimal places.",
            verify_func=validate_task_twenty_eight,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Find the product or products with the largest discount on the home page and follow their stores.",
            verify_func=validate_task_twenty_nine,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Create a new shopping list named 'Coffee' and add the coffee-related items from the home page to that list.",
            verify_func=validate_task_thirty,
            human_steps=15,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Find the cheapest electronics item in the cart, check out using 'Credit' as the payment method, and ship it to William White's address.",
            verify_func=validate_task_thirty_one,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add 1 'Apple MacBook Air 13-inch with M4 Chip, Silver, M4 / 16GB / 256GB', 2 'Apple MacBook Air 13-inch with M4 Chip, Midnight, M4 / 16GB / 512GB', and 3 'Apple MacBook Air 13-inch with M4 Chip, Starlight, M4 / 16GB / 1TB' to the cart.",
            verify_func=validate_task_thirty_two,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Send the following messages to customer service: 'Hi', 'I have a question about my order', and 'I want to cancel'. Tell me how many customer service replies you received, and return only an Arabic numeral.",
            verify_func=validate_task_thirty_three,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Check out all unpaid orders.",
            verify_func=validate_task_thirty_four,
            human_steps=17,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add the Food item with the most reviews from the Interests page to the cart, then check it out and send it to Patricia Harris's address.",
            verify_func=validate_task_thirty_five,
            human_steps=14,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Calculate the average price of items in each shopping list and give the lowest average price rounded to two decimal places.",
            verify_func=validate_task_thirty_six,
            human_steps=17,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Create a shopping list named 'Electronics Wishlist', then search for 'Samsung' and add the first search result to that list.",
            verify_func=validate_task_thirty_seven,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Confirm receipt for all shipped orders.",
            verify_func=validate_task_thirty_eight,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Search for 'food', find the best-selling product, add its highest-priced option to the cart, and check out.",
            verify_func=validate_task_thirty_nine,
            human_steps=13,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Buy the most heavily discounted item on the repurchase page and check out.",
            verify_func=validate_task_forty,
            human_steps=12,
            is_reasoning=True,
        ),
    ],
)
