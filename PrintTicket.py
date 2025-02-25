from fasthtml.common import *
from BackEnd import *

def register_routes(rt):
    @rt("/ticket")
    def get():
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
                        P("Payment Reference: ", Strong("1700009781")),
                        Class="header"
                    ),
                    Div(
                        Button("Print Ticket", Class="button", onclick="location.href='/'"),
                    ),
                    Class="container"
                ),
                Card(
                    Div(
                        H3("Thai Bus Transport"),
                        P("Booking Code: ", Span("THSBSXR15515", Class="highlight")),
                        P(Strong("Date: "), "Friday, September 24, 2021"),
                        P(Strong("Departure: "), "08:00 - Bangkok Bus Terminal"),
                        P(Strong("Arrival: "), "18:00 - Krabi Bus Terminal"),
                        P(Strong("Passenger: "), "Mr. Kasidit Chongrak (Seat A1)"),
                        Class="ticket-info"
                    ),
                    Div(
                        H3("Payment Summary"),
                        P(Strong("Adult Ticket: "), "776.00 THB"),
                        P(Strong("Processing Fee: "), "20.00 THB"),
                        P(Strong("Discount: "), "-100.00 THB"),
                        H3("Total: 696.00 THB"),
                        Class="payment"
                    )
                )
                
            )
        )
        return page

