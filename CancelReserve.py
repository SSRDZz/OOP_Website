from fasthtml.common import *
from BackEnd import *


def register_routes(rt):

    @rt("/cancel-resevation/{booking_id}")
    def get(booking_id:str):
        current_booked = website.current_user.search_booking(booking_id)
        
        page = Div(
            Head(
                Title("Cancel Reservation")
            ),
            Body(
                H1("Cancel Reservation"),
                P("Are you sure you want to cancel your reservation?"),
                Div(
                    Button("Yes, Cancel", onclick=f"location.href='/cancel-resevation/{current_booked.booking_id}/update_status_cancel'"),
                    Button("No, Go Back", onclick="window.history.back()"),
                    style="display: flex; justify-content: space-around; margin-top: 20px;"
                ),
                style="text-align: center; margin-top: 50px;"
            )
        )
        
        return page


