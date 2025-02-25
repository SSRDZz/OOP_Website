from fasthtml.common import *
from dataclasses import dataclass
from BackEnd import *

# FastHTML app setup----------------------
app, rt = fast_app()

@rt('/')
def get():
   return Form(H3("ค้นหาทัวร์สุดพิเศษ"),
            Group(
                     
                Input(name="tour_place",placeholder="ชื่อสถานที่"),
                Input(name="tour_id",type="number",placeholder="รหัสทัวร์"),
                Input(name="tour_time",placeholder="วันที่"),
                

                style="max-width: 75%; margin: 0 auto;"
                
                # 
        ),
        Button("Search"),
        method="GET", action="/tour-results"
   )

@rt('/tour-results')
def get(tour_place="", tour_id="", tour_time=""):

    tours = website.SearchTour(id=tour_id, time=tour_time, place=tour_place)
    try:
        for tour in tours:
            print(tour.name)
    except:
        print("tours = 0\n\n\n")

    if(tours!=None or tours!=[]):
        return Div(
            H2("ผลลัพธ์การค้นหา"),
            *[Card(H3(tour.id),P(tour.name), P(tour.place),P(tour.time)) for tour in tours],
            Button("ย้อนกลับ", onclick="window.location.href='/'")  
        )
    else:
        return Div(H2("ไม่พบผลลัพธ์"), Button("ย้อนกลับ", onclick="window.location.href='/'")  )



serve()
