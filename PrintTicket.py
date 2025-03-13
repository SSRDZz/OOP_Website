from fasthtml.common import *
from BackEnd import *

user = website.current_user

def register_routes(rt):
    
    def show_payment_information(current_booked, payment):
        name = current_booked.data.split('|')[0].split(':')[1] + " " + current_booked.data.split('|')[1].split(':')[1]
        place = current_booked.tour_program.place
        date = current_booked.tour_program.time
        adults = current_booked.data.split('|')[4].split(':')[1]
        children = current_booked.data.split('|')[5].split(':')[1]
        total_price = payment.net_price
        payment_method = payment.payment_method

        return Div(
            P(Strong("Payment Method: "), Span(payment_method)),
            P(Strong("Location: "), Span(place)),
            P(Strong("Date: "), Span(date)),
            P(Strong("Booker: "), Span(name)),
            P(Strong("Adults: "), Span(adults)),
            P(Strong("Children: "), Span(children)),
            P(Strong("Total Price: "), Span(f"{total_price:,.2f} THB")),
            Class="payment-info"
        )


    @rt("/ticket/{booking_id}")
    def get(booking_id: str):
        user = website.current_user
        current_booked = user.search_booking(booking_id)
        payment = user.search_payment(booking_id) 
        
        transaction_id = current_booked.booking_id
        name = current_booked.tour_program.name
        date = current_booked.tour_program.time
        page = Div(
            Head(
                Style("""
                    body { font-family: Arial, sans-serif; }
                    .container { width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
                    .header { display: flex; justify-content: space-between; align-items: center; }
                    .ticket-info { margin-top: 20px; }
                    .highlight { font-weight: bold; color: red; }
                    .payment { margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px; }
                    .button { padding: 10px; font-size: 16px; border: 1px solid;cursor: pointer; text-align: center; }
                    .print-button { background-color: #ffffff; color: orange; font-weight: bold; }
                    .print-button:hover { background-color: orange; color: #ffffff; }
                    .back-button { background-color: #f0f0f0; color: #000000; font-weight: bold; }
                    .back-button:hover { background-color: #d0d0d0; }
                    .modal { display: none; position: fixed; z-index: 1; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.4); }
                    .modal-content { background-color: #fefefe; margin: 10% auto; padding: 20px; border: 1px solid #888; width: 50%; }
                    .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
                    .close:hover { color: black; }
                    .payment-info { border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #f9f9f9; margin-top: 10px; }
                """)
            ),
            Body(
                Div(
                    Div(
                        H2("Booking Ticket"),
                        P("Transaction ID: ", Strong(transaction_id)),
                        Class="header"
                    ),
                    Div(
                        P("Transaction ID: ", Span(transaction_id, Class="highlight")),
                        P(Strong("Tour: "), Span(name)),
                        P(Strong("Date: "), Span(date)),
                        P(Strong("Payment Info: "), show_payment_information(current_booked, payment)),
                        Button("Print Ticket", Class="button print-button", onclick="window.print()"),
                        Button("Back", Class="button back-button", onclick="window.history.back()"),
                        Class="ticket-info"
                    ),
                    Class="container"
                ),
            )
        )
        
        return page