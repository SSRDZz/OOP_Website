from fasthtml.common import *
from BackEnd import *

def register_routes(rt):

    from Payment import register_routes as register_pay
    from PrintTicket import register_routes as register_ticket
    from CancelReserve import register_routes as register_cancel
    
    register_pay(rt)
    register_ticket(rt)
    register_cancel(rt)

    user = website.current_user  # easier to access
    
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
                
        return Tr(
            Td(f"{booked.tour_program.name}"),
            Td(f"{booked.tour_program.time}"),
            Td(updateStatus(booked, status)),  # ["pending", "payment", "done", "canceled"]
            Td(Button("พิมพ์ตั๋ว", disabled=status != "done", onclick=f"location.href='/ticket/{booked.booking_id}'", style="background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; cursor: pointer;")),
            Td(Button("ยกเลิก", disabled=status in ["pending","canceled", "done"], onclick=f"location.href='/cancel-resevation/{booked.booking_id}'", style="background-color: #f44336; color: #fff; padding: 10px 20px; border: none; cursor: pointer;"))
        )

    @rt('/payment/{booking_id}/update_status_done/')
    def get(booking_id: str):
        user = website.current_user
        current_booked = user.search_booking(booking_id)    
        current_booked.update_status = "done" 
        return Redirect("/reserve-history")

    @rt('/cancel-resevation/{booking_id}/update_status_cancel/')
    def get(booking_id: str):
        user = website.current_user
        current_booked = user.search_booking(booking_id)
        current_booked.update_status = "canceled" 
        return Redirect("/reserve-history")

    @rt('/reserve-history')
    def get():
        user = website.current_user  # Ensure the current user is fetched here
        page = Div(
            Head(
                Title("History Page"),
                Style("""
                    html, body {
                        height: 100%;
                        margin: 0;
                        padding: 0;
                        background-color: #ffffff;
                        color: #fff; /* Change text color to white for better contrast */
                        font-family: Arial, sans-serif;
                    }
                    .back-button {
                        background-color: #FFD700;
                        color: #000000;
                        padding: 10px;
                        font-size: 16px;
                        cursor: pointer;
                        text-align: center;
                        margin: 10px;
                    }
                    .back-button:hover {
                        background-color: #ccac00;
                    }
                    .header {
                        color: black;
                        padding: 25px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    .header .title {
                        font-size: 30px;
                        font-weight: bold;
                    }
                    .content {
                        padding: 20px;
                    }
                    .table-container {
                        width: 100%;
                        overflow-x: auto;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }
                    th, td {
                        padding: 12px;
                        border: 1px solid #ddd;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                """)
            ),
            Div(
                Div("History", Class="title"),
                Button("Back to Main Page", Class="back-button", onclick="location.href='/MainPage'"),
                Class="header"
            ),
            Div(
                Div(
                    Table(
                        Tr(
                            Th("Tour"),
                            Th("Date"),
                            Th("Status"),
                            Th("พิมพ์ตั๋ว"),
                            Th("ยกเลิกการจอง")
                        ),
                        *[renderHistory(booked) for booked in user.booking_list]
                    ),
                    Class="table-container"
                ),
                style="margin: 15px; position: relative;"
            ),
            style="height : 100vh"
        
        )
        return page