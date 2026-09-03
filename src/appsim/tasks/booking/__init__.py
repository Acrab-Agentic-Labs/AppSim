# All instructions: file index equals task index
# type: ignore
# noqa
from ..base import AppTasks, TaskItem


from .eval_1 import verify_hotel_booking_created_for_requested_date
from .eval_2 import verify_highest_rated_hotel_booking_created
from .eval_3 import verify_most_expensive_hotel_booking_created
from .eval_4 import verify_last_stay_five_star_review_submitted
from .eval_5 import verify_four_star_hotel_with_shuttle_booking_created
from .eval_6 import verify_repeat_hotel_booking_with_room_note
from .eval_7 import verify_cheapest_flight_booking_created
from .eval_8 import verify_first_class_flight_without_extra_baggage
from .eval_9 import verify_premium_economy_flight_booking_created
from .eval_10 import verify_flight_search_without_booking
from .eval_11 import verify_airport_car_pickup_booking_created
from .eval_12 import verify_economy_suv_rental_booking_created
from .eval_13 import verify_rental_car_with_child_seat
from .eval_14 import verify_cheapest_comfort_sedan_rental
from .eval_15 import verify_immediate_taxi_booking_created
from .eval_16 import verify_round_trip_taxi_bookings_created
from .eval_17 import verify_most_comfortable_taxi_booking_created
from .eval_18 import verify_most_expensive_attraction_vip_ticket
from .eval_19 import verify_attraction_standard_ticket_booking
from .eval_20 import verify_fast_track_attraction_ticket_booking
from .eval_21 import verify_nearest_upcoming_trip, TASK21_ANSWER_SCHEMA
from .eval_22 import verify_profile_phone_updated
from .eval_23 import verify_total_spending_amount, TASK23_ANSWER_SCHEMA
from .eval_24 import verify_future_bookings_canceled
from .eval_25 import verify_profile_first_name_updated

BOOKING_TASKS = AppTasks(
    package_name="com.example.booking",
    task_items=[
        TaskItem(
            instruction='Book me a hotel in London for next Saturday night for two people.',
            verify_func=verify_hotel_booking_created_for_requested_date,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to stay tomorrow night at the highest-rated hotel in London.',
            verify_func=verify_highest_rated_hotel_booking_created,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to stay the night after tomorrow at the most expensive hotel in London.',
            verify_func=verify_most_expensive_hotel_booking_created,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Leave a five-star review for the hotel I stayed at last time.',
            verify_func=verify_last_stay_five_star_review_submitted,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a hotel in London for the night after tomorrow: it must be a 4-star hotel with airport shuttle service and not too expensive.',
            verify_func=verify_four_star_hotel_with_shuttle_booking_created,
            human_steps=17,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to stay tomorrow night at the same hotel as my last stay, and add a note saying no end room.',
            verify_func=verify_repeat_hotel_booking_with_room_note,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me the cheapest flight from Wuhan to London.',
            verify_func=verify_cheapest_flight_booking_created,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a first-class flight from Hong Kong International Airport to London Heathrow Airport, and confirm that I do not need extra baggage allowance.',
            verify_func=verify_first_class_flight_without_extra_baggage,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a premium economy flight from London to Sydney.',
            verify_func=verify_premium_economy_flight_booking_created,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I might need to fly from London to Hong Kong next Sunday, but I am not sure yet.',
            verify_func=verify_flight_search_without_booking,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a rental car with pickup at London Heathrow Airport at noon the day after tomorrow.',
            verify_func=verify_airport_car_pickup_booking_created,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I am at London Heathrow Airport now. Rent me an economy SUV through next Monday.',
            verify_func=verify_economy_suv_rental_booking_created,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I want to rent a car when I land at Hong Kong International Airport at noon the day after tomorrow. I am traveling with a child, so add a child safety seat.',
            verify_func=verify_rental_car_with_child_seat,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I will arrive at Hong Kong International Airport at noon the day after tomorrow. Please rent the cheapest comfort sedan.',
            verify_func=verify_cheapest_comfort_sedan_rental,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I just landed at London Heathrow Airport. Book me a taxi to the London Heathrow Airport Hilton Hotel now.',
            verify_func=verify_immediate_taxi_booking_created,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='I will be transiting at London Heathrow Airport tomorrow at noon. Book a taxi then to the London Heathrow Airport Hilton Hotel, and another ride at 8:00 AM the day after tomorrow back to London Heathrow Airport.',
            verify_func=verify_round_trip_taxi_bookings_created,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a taxi right now from Hong Kong International Airport to the Regal Airport Hotel, and choose the most comfortable car.',
            verify_func=verify_most_comfortable_taxi_booking_created,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a VIP ticket for the most expensive attraction in Paris for the day after tomorrow.',
            verify_func=verify_most_expensive_attraction_vip_ticket,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a standard ticket to Sagrada Familia.',
            verify_func=verify_attraction_standard_ticket_booking,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Book me a fast-track ticket for a green-themed attraction in London for tomorrow.',
            verify_func=verify_fast_track_attraction_ticket_booking,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Tell me what my nearest upcoming trip is.',
            verify_func=verify_nearest_upcoming_trip,
            human_steps=1,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK21_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Change my phone number to 752-0405.',
            verify_func=verify_profile_phone_updated,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Calculate how much I have spent so far.',
            verify_func=verify_total_spending_amount,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="hybrid",
            answer_schema=TASK23_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='Cancel all bookings scheduled after next month.',
            verify_func=verify_future_bookings_canceled,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='Update my profile first name to Peter.',
            verify_func=verify_profile_first_name_updated,
            human_steps=5,
            is_reasoning=False,
        ),
    ],
)
