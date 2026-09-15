from ..base import AppTasks, TaskItem
from .eval_1 import verify_first_search_result_added_to_cart
from .eval_2 import verify_cart_total_price, TASK2_ANSWER_SCHEMA
from .eval_3 import verify_interests_category_item_count, TASK3_ANSWER_SCHEMA
from .eval_4 import verify_customer_service_message_sent
from .eval_5 import verify_order_count, TASK5_ANSWER_SCHEMA
from .eval_6 import verify_product_variant_added_to_cart
from .eval_7 import verify_shopping_list_created
from .eval_8 import verify_shipping_address_deleted
from .eval_9 import verify_product_purchased_with_gift_card
from .eval_10 import verify_store_followed
from .eval_11 import verify_highest_rated_category_product_added_to_cart
from .eval_12 import verify_lowest_price_product_purchased_and_shipped
from .eval_13 import verify_shipping_address_phone_updated
from .eval_14 import verify_canceled_order_total_amount, TASK14_ANSWER_SCHEMA
from .eval_15 import verify_pending_orders_canceled
from .eval_16 import verify_first_order_items_reordered
from .eval_17 import verify_low_price_cart_items_removed
from .eval_18 import verify_customer_service_return_period, TASK18_ANSWER_SCHEMA
from .eval_19 import verify_search_result_review_keyword_count, TASK19_ANSWER_SCHEMA
from .eval_20 import verify_high_rated_search_result_count, TASK20_ANSWER_SCHEMA
from .eval_21 import verify_cheapest_repurchase_item_added_to_cart
from .eval_22 import verify_three_most_expensive_cart_items_total, TASK22_ANSWER_SCHEMA
from .eval_23 import verify_most_reviewed_shopping_list_item_added_to_cart
from .eval_24 import verify_most_expensive_cart_item_purchased
from .eval_25 import verify_most_discounted_home_item_purchased
from .eval_26 import verify_first_search_result_purchased_and_address_selected
from .eval_27 import verify_default_shipping_address_added
from .eval_28 import verify_highest_interests_category_average_rating, TASK28_ANSWER_SCHEMA
from .eval_29 import verify_most_discounted_home_items_stores_followed
from .eval_30 import verify_shopping_list_created_with_home_items
from .eval_31 import verify_cheapest_cart_electronics_item_purchased
from .eval_32 import verify_requested_item_quantities_added_to_cart
from .eval_33 import verify_customer_service_response_count, TASK33_ANSWER_SCHEMA
from .eval_34 import verify_unpaid_orders_checked_out
from .eval_35 import verify_most_reviewed_category_item_purchased_and_shipped
from .eval_36 import verify_lowest_shopping_list_average_price, TASK36_ANSWER_SCHEMA
from .eval_37 import verify_search_result_added_to_shopping_list
from .eval_38 import verify_shipped_orders_receipt_confirmed
from .eval_39 import verify_highest_sales_product_purchased
from .eval_40 import verify_most_discounted_repurchase_item_purchased

AMAZON_TASKS = AppTasks(
    package_name="com.example.amazon_sim",
    task_items=[
        TaskItem(
            instruction="Search for 'ball' on the home page, view the search results, and add the first item to the cart.",
            verify_func=verify_first_search_result_added_to_cart,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Calculate the total price of the items in the cart and return only an Arabic numeral.",
            verify_func=verify_cart_total_price,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check how many 'Lifestyle' items are in the Interests section and return only an Arabic numeral.",
            verify_func=verify_interests_category_item_count,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Send 'Hello, I have some questions about Dyson products.' to customer service.",
            verify_func=verify_customer_service_message_sent,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="View my order list, calculate how many orders I have in total, and return only an Arabic numeral.",
            verify_func=verify_order_count,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Select the 12 oz option of Starbucks coffee beans and add it to the cart.",
            verify_func=verify_product_variant_added_to_cart,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Create a new shopping list named 'My Amazon List'.",
            verify_func=verify_shopping_list_created,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Delete the fourth shipping address.",
            verify_func=verify_shipping_address_deleted,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Buy a white Nintendo Switch now and check out using Amazon Gift Card.",
            verify_func=verify_product_purchased_with_gift_card,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Follow the Marshall store.",
            verify_func=verify_store_followed,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Find the highest-rated product in the 'Lifestyle' category and add it to the cart.",
            verify_func=verify_highest_rated_category_product_added_to_cart,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Buy a watch from the home page right away, choose the lowest-priced option, and have it shipped to Sarah Davis's address.",
            verify_func=verify_lowest_price_product_purchased_and_shipped,
            human_steps=10,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Change the phone number for Robert Taylor's address to '+1(555)613-1230'.",
            verify_func=verify_shipping_address_phone_updated,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="View the canceled order and tell me its total amount.",
            verify_func=verify_canceled_order_total_amount,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK14_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Cancel all pending orders.",
            verify_func=verify_pending_orders_canceled,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Buy the items from the first order again.",
            verify_func=verify_first_order_items_reordered,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Remove all items priced below $200 from the cart.",
            verify_func=verify_low_price_cart_items_removed,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Send 'I want to return my order' to customer service, then check and tell me how many days are mentioned in the reply as the return period. Return only an Arabic numeral.",
            verify_func=verify_customer_service_return_period,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK18_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Search for 'MacBook' and tell me how many reviews mention 'Battery life' in the result item. Return only an Arabic numeral.",
            verify_func=verify_search_result_review_keyword_count,
            human_steps=6,
            is_reasoning=False,
            evaluation_type="answer",
            answer_schema=TASK19_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Search for 'electronics', count how many items have a rating higher than 4.8, and return only an Arabic numeral.",
            verify_func=verify_high_rated_search_result_count,
            human_steps=7,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK20_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="View the items available for repurchase, find the cheapest one, and add it to the cart.",
            verify_func=verify_cheapest_repurchase_item_added_to_cart,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="In the cart, find the three most expensive items by unit price, calculate their total price, and return only an Arabic numeral.",
            verify_func=verify_three_most_expensive_cart_items_total,
            human_steps=8,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK22_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Add the item with the most reviews from the list 'Shopping List 2' to the cart.",
            verify_func=verify_most_reviewed_shopping_list_item_added_to_cart,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Check out the most expensive item in the cart.",
            verify_func=verify_most_expensive_cart_item_purchased,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Buy the most heavily discounted electronics item on the home page right away.",
            verify_func=verify_most_discounted_home_item_purchased,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Search for 'Dyson', open the first product detail page and purchase immediately. Then, check out using Sarah Davis's address.",
            verify_func=verify_first_search_result_purchased_and_address_selected,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add a new shipping address for recipient 'Alex Johnson', phone number '3105550199', address '123 Main St, Apt 8C, Los Angeles, California', ZIP code '90012', and set it as the default address.",
            verify_func=verify_default_shipping_address_added,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="On the Interests page, check each of the four categories, calculate the average rating of all products in each category, and give me the highest average rating rounded to two decimal places.",
            verify_func=verify_highest_interests_category_average_rating,
            human_steps=12,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK28_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Find the product or products with the largest discount on the home page and follow their stores.",
            verify_func=verify_most_discounted_home_items_stores_followed,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Create a new shopping list named 'Coffee' and add the coffee-related items from the home page to that list.",
            verify_func=verify_shopping_list_created_with_home_items,
            human_steps=15,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Find the cheapest electronics item in the cart, check out using 'Credit' as the payment method, and ship it to William White's address.",
            verify_func=verify_cheapest_cart_electronics_item_purchased,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Add 1 'Apple MacBook Air 13-inch with M4 Chip, Silver, M4 / 16GB / 256GB', 2 'Apple MacBook Air 13-inch with M4 Chip, Midnight, M4 / 16GB / 512GB', and 3 'Apple MacBook Air 13-inch with M4 Chip, Starlight, M4 / 24GB / 1TB' to the cart.",
            verify_func=verify_requested_item_quantities_added_to_cart,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Send 'Hi', 'I have a question about my order', and 'I want to cancel' to the customer service one by one. Let me know how many customer service responses you have received in total, excluding the initial greeting message from the customer service. Please return the number in Arabic numerals only.",
            verify_func=verify_customer_service_response_count,
            human_steps=11,
            is_reasoning=False,
            evaluation_type="hybrid",
            answer_schema=TASK33_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Check out all unpaid orders.",
            verify_func=verify_unpaid_orders_checked_out,
            human_steps=17,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Add the Food item with the most reviews from the Interests page to the cart, then check it out and send it to Patricia Harris's address.",
            verify_func=verify_most_reviewed_category_item_purchased_and_shipped,
            human_steps=14,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Calculate the average price of items in each shopping list and give the lowest average price rounded to two decimal places.",
            verify_func=verify_lowest_shopping_list_average_price,
            human_steps=17,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK36_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="Create a shopping list named 'Electronics Wishlist', then search for 'Samsung' and add the first search result to that list.",
            verify_func=verify_search_result_added_to_shopping_list,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Confirm receipt for all shipped orders.",
            verify_func=verify_shipped_orders_receipt_confirmed,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="Search for 'food', find the product with the highest sales volume, immediately purchase the highest-priced specification of it and complete the checkout.",
            verify_func=verify_highest_sales_product_purchased,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="Buy the most heavily discounted item on the repurchase page and check out.",
            verify_func=verify_most_discounted_repurchase_item_purchased,
            human_steps=12,
            is_reasoning=True,
        ),
    ],
)
