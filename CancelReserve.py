from fasthtml.common import *
from BackEnd import *


def register_routes(rt):

    @rt("/cancel-resevation")
    def get():
        
        page = Div(
            Head(
                Title("Cancel Reservation")
            ),
            Body(
                H1("Cancel Reservation"),
                P("Are you sure you want to cancel your reservation?"),
                Div(
                    Button("Yes, Cancel", onclick="location.href='/update_status_cancel'"),
                    Button("No, Go Back", onclick="location.href='/'"),
                    style="display: flex; justify-content: space-around; margin-top: 20px;"
                ),
                style="text-align: center; margin-top: 50px;"
            )
        )
        
        return page


