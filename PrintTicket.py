from fasthtml.common import *
from BackEnd import *

user = website.currentUser

def register_routes(rt):
    @rt("/ticket/{booking_id}")
    def get(booking_id: str):
        
        current_booked = website.currentUser.search_booking(booking_id)
        
        booking_code = current_booked.booking_id
        tour_name = current_booked.tour_program.name
        tour_date = current_booked.tour_program.time
        departure_time = current_booked.tour_program.departure_time if hasattr(current_booked.tour_program, 'departure_time') else "N/A"
        arrival_time = current_booked.tour_program.arrival_time if hasattr(current_booked.tour_program, 'arrival_time') else "N/A"
        departure_location = current_booked.tour_program.departure_location if hasattr(current_booked.tour_program, 'departure_location') else "N/A"
        arrival_location = current_booked.tour_program.arrival_location if hasattr(current_booked.tour_program, 'arrival_location') else "N/A"
        passenger_name = user.username
        seat_number = current_booked.seat_number if hasattr(current_booked, 'seat_number') else "N/A"
        total_price = current_booked.total_price if hasattr(current_booked, 'total_price') else "N/A"

        page = Div(
            Head(
                Style("""
                    body { font-family: Arial, sans-serif; }
                    .container { width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
                    .header { display: flex; justify-content: space-between; align-items: center; }
                    .ticket-info { margin-top: 20px; }
                    .highlight { font-weight: bold; color: red; }
                    .payment { margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px; }
                    .button { background-color: #ffffff; color: orange; font-weight: bold; padding: 10px; font-size: 16px; border: solid; cursor: pointer; text-align: center; }
                """)
            ),
            Body(
                Div(
                    Div(
                        H2("Booking Ticket"),
                        P("Payment Reference: ", Strong(f"{booking_code}")),
                        Class="header"
                    ),
                    Div(
                        Button("Print Ticket", Class="button", onclick="location.href='/'"),
                        
                    ),
                    Class="container"
                ),
                Card(
                    Div(
                        H3(tour_name),
                        P("Booking Code: ", Span(booking_code, Class="highlight")),
                        P(Strong("Date: "), tour_date),
                        P(Strong("Departure: "), f"{departure_time} - {departure_location}"),
                        P(Strong("Arrival: "), f"{arrival_time} - {arrival_location}"),
                        P(Strong("Passenger: "), f"{passenger_name} (Seat {seat_number})"),
                        Class="ticket-info"
                    ),
                    Div(
                        H3("Payment Summary"),
                        P(Strong("Total: "), f"{total_price} THB"),
                        Class="payment"
                    )
                )
            )
        )
        return page