from fasthtml.common import *
from BackEnd import *
from Payment import register_routes as register_pay
from PrintTicket import register_routes as register_ticket


app, rt = fast_app()

register_pay(rt)
register_ticket(rt)
    
#Test Instance
user = User("Pongsak", "1234")
user.create_booking_tour(website.SearchTour(1), None)

status = "payment"


def updateStatus(status):
    if status == "pending":
        return P("Pending...", style="color: #d4bc08")
    elif status == "done":
        return P("Done", style="color: #0cad5d")
    elif status == "payment":
        content = Button("จ่ายเงิน",onclick="location.href='/payment'")  
        return content
    elif status == "canceled":
        return P("Canceled", style="color: #8c8787")
    
    else :
        return "Error"

def renderHistory(booked):
    
    # booked.update_status = "payment"  
    global status
    
    return  Body(  
                Card( 
                    Grid(
                        Div(f"{booked.tour_program.name}"),  
                        Div(f"{booked.tour_program.time}"),  
                        Div(updateStatus(status)),                          #["pending", "payment", "done", "canceled"]    
                        Div(Button("พิมพ์ตั๋ว",onclick="location.href='/ticket'")),  
                        Div(Button("ยกเลิก", ),  #onclick="location.href='/canceled-booked'
                        ),
                        style="display: grid; grid-template-columns: repeat(5, 2fr); text-align: center; align-items: center; "
                    ),
                    style="padding: 10px; margin: 5px; border: 1px solid #ddd;"
                )
            )
 

@rt('/update_status_done/')
def get():
    
    global status
    status = "done"                   # Update the status to 'done' after successful payment

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

serve()
