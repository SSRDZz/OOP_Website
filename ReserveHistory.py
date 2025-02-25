from fasthtml.common import *
from BackEnd import *

app, rt = fast_app()


class User(Account):
    def __init__(self,name,password):
        self.__booking = []
        super().__init__(name,password)
        print("User created :",self.username)

    def create_booking_tour(self,tour_program : TourProgram, data):
        self.__booking.append(Booking(tour_program, None))
    
    @property
    def bookingList(self):
        return self.__booking
    
user1 = User("Pongsak", "1234")
user1.create_booking_tour(website.SearchTour(1), None)


def renderHistory():
    return  Body(
                  
                Card( 
                    Grid(
                        Div(f"{user1.bookingList[0].tour_program.name}"),  
                        Div(f"{user1.bookingList[0].tour_program.time}"),  
                        Div("(pending, ปุ่มชำระเงิน, success)"),  
                        Div(Button("พิมพ์ตั๋ว",hx_post="")),  
                        Div(Button("ยกเลิก", ),  
                        style="display: grid; grid-template-columns: repeat(5, 2fr); text-align: center; "
                        ),
                    ),
                    style="padding: 10px; margin: 5px; border: 1px solid #ddd;  align-items: center;"
                )
            )





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

        renderHistory(),
        
        
        style="margin: 15px;"
    )
    return page

serve()
