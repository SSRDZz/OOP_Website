from fasthtml.common import *
from BackEnd import *

def register_routes(rt):

    from Payment import register_routes as register_pay
    from PrintTicket import register_routes as register_ticket
    from CancelReserve import register_routes as register_cancel
    
    register_pay(rt)
    register_ticket(rt)
    register_cancel(rt)

    user = website.currentUser  #easier to access
    
    
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
        print(booked.booking_id)
        
        return Tr(
            Td(f"{booked.tour_program.name}"),
            Td(f"{booked.tour_program.time}"),
            Td(updateStatus(booked, status)),  # ["pending", "payment", "done", "canceled"]
            Td(Button("พิมพ์ตั๋ว", disabled=status != "done", onclick=f"location.href='/ticket/{booked.booking_id}'", style="background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; cursor: pointer;")),
            Td(Button("ยกเลิก", disabled=status in ["canceled", "done"], onclick=f"location.href='/cancel-resevation/{booked.booking_id}'", style="background-color: #f44336; color: #fff; padding: 10px 20px; border: none; cursor: pointer;"))
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
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                    }
                    .back-button {
                        background-color: #F5F7F8;
                        color: #000000;
                        font-weight: bold;
                        padding: 10px;
                        font-size: 16px;
                        border: solid;
                        cursor: pointer;
                        text-align: center;
                        border-radius: 5px;
                        margin: 10px;
                    }
                    .back-button:hover {
                        background-color: #d0d0d0;
                    }
                    .header {
                        background-color: #e6c200;
                        color: white;
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
                        *[renderHistory(booked) for booked in user.bookingList]
                    ),
                    Class="table-container"
                ),
                style="margin: 15px; position: relative;"
            ),
        
        )
        return page