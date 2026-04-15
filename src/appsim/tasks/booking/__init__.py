# All instructions: file index equals task index
from ..base import AppTasks, TaskItem

from .eval_1 import verify_book_london_stay_next_saturday
from .eval_2 import verify_book_highest_rated_london_stay_tomorrow
from .eval_3 import verify_book_most_expensive_london_stay_day_after_tomorrow
from .eval_4 import verify_submit_five_star_review_for_last_stay
from .eval_5 import verify_book_london_airport_shuttle_four_star_stay
from .eval_6 import verify_book_again_last_stay_with_no_end_room_note
from .eval_7 import verify_book_cheapest_wuhan_to_london_flight
from .eval_8 import verify_book_hkg_to_lhr_first_class_without_extra_baggage
from .eval_9 import verify_book_lhr_to_sydney_premium_economy
from .eval_10 import verify_search_london_to_hong_kong_next_sunday_without_booking
from .eval_11 import verify_book_car_pickup_lhr_day_after_tomorrow_noon
from .eval_12 import verify_book_lhr_car_until_next_monday
from .eval_13 import verify_book_hkg_car_with_child_seat
from .eval_14 import verify_book_cheapest_comfort_sedan_at_hkg
from .eval_15 import verify_book_taxi_lhr_to_hilton_now
from .eval_16 import verify_book_round_trip_taxi_lhr_hilton_and_return
from .eval_17 import verify_book_most_comfortable_taxi_hkg_to_regal
from .eval_18 import verify_book_paris_most_expensive_vip_ticket
from .eval_19 import verify_book_sagrada_standard_ticket
from .eval_20 import verify_book_london_green_skip_line_ticket_tomorrow
from .eval_21 import verify_answer_nearest_upcoming_trip
from .eval_22 import verify_update_profile_name_to_peter_liu
from .eval_23 import verify_update_phone_to_752_0405
from .eval_24 import verify_calculate_spent_amount
from .eval_25 import verify_cancel_all_orders_after_next_month


BOOKING_TASKS = AppTasks(
    package_name="com.example.booking",
    task_items=[
        TaskItem(
            instruction='Book me a hotel in London for next Saturday night for two people.',
            verify_func=verify_book_london_stay_next_saturday,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to stay tomorrow night at the highest-rated hotel in London.',
            verify_func=verify_book_highest_rated_london_stay_tomorrow,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to stay the night after tomorrow at the most expensive hotel in London.',
            verify_func=verify_book_most_expensive_london_stay_day_after_tomorrow,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Leave a five-star review for the hotel I stayed at last time.',
            verify_func=verify_submit_five_star_review_for_last_stay,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a hotel in London for the night after tomorrow: it must be a 4-star hotel with airport shuttle service and not too expensive.',
            verify_func=verify_book_london_airport_shuttle_four_star_stay,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to stay tomorrow night at the same hotel as my last stay, and add a note saying no end room.',
            verify_func=verify_book_again_last_stay_with_no_end_room_note,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me the cheapest flight from Wuhan to London.',
            verify_func=verify_book_cheapest_wuhan_to_london_flight,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a first-class flight from Hong Kong International Airport to London Heathrow Airport, and confirm that I do not need extra baggage allowance.',
            verify_func=verify_book_hkg_to_lhr_first_class_without_extra_baggage,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a premium economy flight from London to Sydney.',
            verify_func=verify_book_lhr_to_sydney_premium_economy,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I might need to fly from London to Hong Kong next Sunday, but I am not sure yet.',
            verify_func=verify_search_london_to_hong_kong_next_sunday_without_booking,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a rental car with pickup at London Heathrow Airport at noon the day after tomorrow.',
            verify_func=verify_book_car_pickup_lhr_day_after_tomorrow_noon,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I am at London Heathrow Airport now. Rent me an economy SUV through next Monday.',
            verify_func=verify_book_lhr_car_until_next_monday,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to rent a car when I land at Hong Kong International Airport at noon the day after tomorrow. I am traveling with a child, so add a child safety seat.',
            verify_func=verify_book_hkg_car_with_child_seat,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I will arrive at Hong Kong International Airport at noon the day after tomorrow. Please rent the cheapest comfort sedan.',
            verify_func=verify_book_cheapest_comfort_sedan_at_hkg,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I just landed at London Heathrow Airport. Book me a taxi to the London Heathrow Airport Hilton Hotel now.',
            verify_func=verify_book_taxi_lhr_to_hilton_now,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I will be transiting at London Heathrow Airport tomorrow at noon. Book a taxi then to the London Heathrow Airport Hilton Hotel, and another ride at 8:00 AM the day after tomorrow back to London Heathrow Airport.',
            verify_func=verify_book_round_trip_taxi_lhr_hilton_and_return,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a taxi right now from Hong Kong International Airport to the Regal Airport Hotel, and choose the most comfortable car.',
            verify_func=verify_book_most_comfortable_taxi_hkg_to_regal,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a VIP ticket for the most expensive attraction in Paris for the day after tomorrow.',
            verify_func=verify_book_paris_most_expensive_vip_ticket,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a standard ticket to Sagrada Familia.',
            verify_func=verify_book_sagrada_standard_ticket,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a fast-track ticket for a green-themed attraction in London for tomorrow.',
            verify_func=verify_book_london_green_skip_line_ticket_tomorrow,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Tell me what my nearest upcoming trip is.',
            verify_func=verify_answer_nearest_upcoming_trip,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Update my profile name to Peter Liu.',
            verify_func=verify_update_profile_name_to_peter_liu,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Change my phone number to 752-0405.',
            verify_func=verify_update_phone_to_752_0405,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Calculate how much I have spent so far.',
            verify_func=verify_calculate_spent_amount,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='Cancel all bookings scheduled after next month.',
            verify_func=verify_cancel_all_orders_after_next_month,
            human_steps=4,
            is_reasoning=False,
        ),
    ],
)
