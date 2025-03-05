from fasthtml.common import *
from BackEnd import *

user = website.currentUser

def register_routes(rt):
    @rt("/ticket/{booking_id}")
    def get(booking_id: str):
        
        current_booked = website.currentUser.search_booking(booking_id)
        payment = user.search_payment(booking_id) 
        
        transaction_id = current_booked.booking_id
        name = current_booked.tour_program.name
        date = current_booked.tour_program.time
        payment_method = payment.payment_method
        payment_info = payment.info if hasattr(payment, 'info') else "N/A"

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
                        P("Transaction ID: ", Strong(f"{transaction_id}")),
                        Class="header"
                    ),
                    Div(
                        Button("Print Ticket", Class="button", onclick="location.href='/'"),
                    ),
                    Class="container"
                ),
                Card(
                    Div(
                        H3(name),
                        P("Transaction ID: ", Span(transaction_id, Class="highlight")),
                        P(Strong("Date: "), date),
                        P(Strong("Payment Method: "), payment_method),
                        P(Strong("Payment Info: "), payment_info),
                        Class="ticket-info"
                    ),
                    style="padding: 20px; width: 55%;"
                ),
                style="display: flex; justify-content: space-between; margin-top: 20px;"
            ),
            style="font-family: Arial, sans-serif;"
        )
        
        return page