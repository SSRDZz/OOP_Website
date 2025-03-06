from fasthtml.common import *
from BackEnd import *

def register_routes(rt):

    from Payment import register_routes as register_pay
    from PrintTicket import register_routes as register_ticket
    from CancelReserve import register_routes as register_cancel
    
    register_pay(rt)
    register_ticket(rt)
    register_cancel(rt)

    user = website.currentUser
    # status = "payment"
    
    def updateStatus(booked, status):
        if status == "pending":
            return P("Pending...", style="color: #d4bc08")
        elif status == "done":
            return P("Done", style="color: #0cad5d")
        elif status == "payment":
            content = Button("จ่ายเงิน", onclick=f"location.href='/payment/{booked.booking_id}'", style="background-color: #ffcc00; color: #fff; padding: 10px 20px; border: none; cursor: pointer;") #?booking_id={booked.booking_id}
            return content
        elif status == "canceled":
            return P("Canceled", style="color: #8c8787")
        else:
            return "Error"

    def renderHistory(booked):
        status = booked.status
        
        return Body(
            Card(
                Grid(
                    Div(f"{booked.tour_program.name}"),
                    Div(f"{booked.tour_program.time}"),
                    Div(updateStatus(booked, status)),  # ["pending", "payment", "done", "canceled"]
                    Div(Button("พิมพ์ตั๋ว", disabled=status != "done", onclick=f"location.href='/ticket/{booked.booking_id}'", style="background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; cursor: pointer;")),
                    Div(Button("ยกเลิก", disabled=status in ["canceled", "done"], onclick=f"location.href='/cancel-resevation/{booked.booking_id}'", style="background-color: #f44336; color: #fff; padding: 10px 20px; border: none; cursor: pointer;")),
                    style="display: grid; grid-template-columns: repeat(5, 2fr); text-align: center; align-items: center;"
                ),
                style="padding: 10px; margin: 5px; border: 1px solid #ddd;"
            )
        )

    @rt('/payment/{booking_id}/update_status_done/')
    def get(booking_id: str):
        
        current_booked = user.search_booking(booking_id)    
        current_booked.update_status = "done" 
        return Redirect("/reserve-history")

    @rt('/cancel-resevation/{booking_id}/update_status_cancel/')
    def get(booking_id: str):

        current_booked = user.search_booking(booking_id)
        current_booked.update_status = "canceled" 
        return Redirect("/reserve-history")

    @rt('/reserve-history')
    def get():
        page = Div(
            Head(
                Title("Tour Amateur"),
                Style("""
                    .back-button {
                        background-color: #f0f0f0;
                        color: #000000;
                        font-weight: bold;
                        padding: 10px;
                        font-size: 16px;
                        border: solid;
                        cursor: pointer;
                        text-align: center;
                        position: absolute;
                        top: 10px;
                        right: 10px;
                    }
                    .back-button:hover {
                        background-color: #d0d0d0;
                    }
                """)
            ),
            Div(
                Button("Back to Main Page", Class="back-button", onclick="location.href='/MainPage'")
            ),
            Div(
                H1("Web Name"),
                P("ประวัติการจอง"),
                style="padding: 10px; "
            ),
            Grid(
                Card("Tour"),
                Card("Date"),
                Card("Status"),
                Card("พิมพ์ตั๋ว"),
                Card("ยกเลิกการจอง"),
                style="text-align: center;"
            ),
            *[renderHistory(booked) for booked in user.bookingList],
            style="margin: 15px; position: relative;"
        )
        return page