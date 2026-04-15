# Booking Task Evaluation Notes

## Instruction language comparison (updated 2026-04-15)

Data source files:
- Chinese baseline (latest full 25-task run before instruction translation):
  - D:\AndroidStudio\app\android_template\AppSim\scripts\results\booking\Seed-1.5-VL\eval_details_Booking_20260411_115820.jsonl
- English run (after instruction translation):
  - D:\AndroidStudio\app\android_template\AppSim\scripts\results\booking\Seed-1.5-VL\eval_details_Booking_20260413_211121.jsonl

Pass rule:
- A task is counted as passed only when `verify_result == true`.

Comparison result:
- Chinese: 10 / 25 passed
- English: 13 / 25 passed
- Delta: +3 passed tasks after switching to English instructions

Pass task IDs:
- Chinese pass IDs: [1, 2, 4, 7, 19, 21, 22, 23, 24, 25]
- English pass IDs: [1, 2, 4, 5, 11, 14, 15, 16, 19, 21, 22, 23, 24]
- Common pass IDs: [1, 2, 4, 19, 21, 22, 23, 24]
- Chinese-only pass IDs: [7, 25]
- English-only pass IDs: [5, 11, 14, 15, 16]

Note:
- There is another older Chinese full run:
  - eval_details_Booking_20260410_135015.jsonl (14 / 25 passed)
- If this older run is used as baseline, English is -1 task.

## Agent returns for non-passing tasks (English run)

Source file:
- D:\AndroidStudio\app\android_template\AppSim\scripts\results\booking\Seed-1.5-VL\eval_details_Booking_20260413_211121.jsonl

Non-passing tasks are:
- [3, 6, 7, 8, 9, 10, 12, 13, 17, 18, 20, 25]

Returned messages (`result.final_message`) and status:
- Task 3 (success=true): "I have successfully selected the most expensive hotel in London for your stay the night after tomorrow: The Kensington Grand, with its highest-priced Suite room at $780 per night. The booking process is now at the personal information stage, ready for you to fill in your details to complete the reservation."
- Task 6 (success=false): final_message = null; error field exists but stored as garbled text (`?????????`) in this log export.
- Task 7 (success=true): "I have selected the cheapest flight from Wuhan to London (Turkish Airlines, $620) and navigated to the traveler details page. To complete the booking, please provide the gender specified on your passport/ID, as this field is required to proceed and enable the \"Done\" button."
- Task 8 (success=true): "I have successfully selected a first-class flight from Hong Kong International Airport to London Heathrow Airport. The chosen fare includes only carry-on baggage, so no extra baggage allowance is needed. The booking process is now at the traveler details step, and the core requirements of the task have been fulfilled."
- Task 9 (success=true): "I was unable to find a premium economy flight option from London to Sydney in the available search results. The displayed flights only offer economy class fares (Basic, Value, Comfort). Please adjust your search criteria or try again later."
- Task 10 (success=false): final_message = null; error field exists but stored as garbled text (`?????????`) in this log export.
- Task 12 (success=true): "I have successfully found economy SUV rental options for you at London Heathrow Airport, available through next Monday. The results include a Nissan Qashqai or similar economy SUV from Europcar (rated 7.6 with 1448 reviews, $76/day with free cancellation) and another Nissan Qashqai or similar option with a 12% discount. You can proceed to select and book the one that suits your needs."
- Task 13 (success=true): "Your car rental request has been set up successfully: pickup at Hong Kong International Airport at noon on Apr 17 (the day after tomorrow), return at the same location on Apr 20 at noon, with a child safety seat added. You can now proceed to confirm the booking if you are ready."
- Task 17 (success=true): "Your Premium taxi from Hong Kong International Airport to Regal Airport Hotel has been successfully booked. The trip details are: Date: Apr 13, 2026, Passengers: 2, Price: $25, Order ID: taxi_4062ee36-f8bb-4897-b488-ec65e7cb325e. You can view the trip in the \"Trips\" section if needed."
- Task 18 (success=true): "I'm unable to retrieve attractions in Paris despite multiple search attempts. The results consistently show non-Paris attractions, so I can't proceed to find and book the most expensive VIP attraction in Paris for the day after tomorrow."
- Task 20 (success=true): "I cannot find any green-themed attractions in London with fast-track tickets available for tomorrow on Booking.com. The search results consistently show non-London attractions despite setting the location filter to London and using relevant keywords."
- Task 25 (success=false): final_message = null; error field exists but stored as garbled text (`?????????`) in this log export.
