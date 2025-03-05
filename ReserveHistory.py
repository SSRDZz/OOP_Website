from fasthtml.common import *
from BackEnd import *

from Payment import register_routes as register_pay
from PrintTicket import register_routes as register_ticket
from CancelReserve import register_routes as register_cancel

app, rt = fast_app()    #        pico=False,live=True

register_pay(rt)
register_ticket(rt)
register_cancel(rt)

user = website.currentUser
# status = "payment"

def updateStatus(booked,status):
    if status == "pending":
        return P("Pending...", style="color: #d4bc08")
    elif status == "done":
        return P("Done", style="color: #0cad5d")
    elif status == "payment":
        content = Button("จ่ายเงิน", onclick=f"location.href='/payment/{booked.booking_id}'") #?booking_id={booked.booking_id}
        return content
    elif status == "canceled":
        return P("Canceled", style="color: #8c8787")
    else:
        return "Error"

def renderHistory(booked):
    # global status
    
    status = booked.status
    
    return Body(
        Card(
            Grid(
                Div(f"{booked.tour_program.name}"),
                Div(f"{booked.tour_program.time}"),
                Div(updateStatus(booked,status)),  # ["pending", "payment", "done", "canceled"]
                Div(Button("พิมพ์ตั๋ว", disabled=status != "done", onclick=f"location.href='/ticket/{booked.booking_id}'")),
                Div(Button("ยกเลิก", disabled=status in ["canceled", "done"], onclick=f"location.href='/cancel-resevation/{booked.booking_id}'")),
                style="display: grid; grid-template-columns: repeat(5, 2fr); text-align: center; align-items: center;"
            ),
            style="padding: 10px; margin: 5px; border: 1px solid #ddd;"
        )
    )

@rt('/payment/{booking_id}/update_status_done/')
def get(booking_id:str):
    
    current_booked = user.search_booking(booking_id)    
    current_booked.update_status = "done" 
    return Redirect("/")

@rt('/cancel-resevation/{booking_id}/update_status_cancel/')
def get(booking_id:str):
  
    current_booked = user.search_booking(booking_id)
    current_booked.update_status = "canceled" 
    return Redirect("/")

@rt('/')
def get():
    page = Div(
        Head(
            Title("Tour Amateur"),
            style="""
            
            """
        ),
        Div(
            H1("Web Name"),
            P("ประวัติการจอง"),
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
        style="margin: 15px;"
    )
    return page

if __name__ == "__main__":
    serve()