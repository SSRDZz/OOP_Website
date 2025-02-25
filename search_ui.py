from fasthtml.common import *
from dataclasses import dataclass
from BackEnd import *

# FastHTML app setup----------------------
app, rt = fast_app()

@rt('/')
def get():
   return Form(H3("ค้นหาทัวร์สุดพิเศษ"),
            Group(
                     
                Label(Input(id="tour_place",type="text",placeholder="ชื่อสถานที่")),
                Label(Input(id="tour_id",type="text",placeholder="รหัสทัวร์")),
                Label(Input(id="tour_time",type="text",placeholder="วันที่")),
                

                style="max-width: 75%; margin: 0 auto;"
                
                # 
            ),
        Button("Search"
             # ส่งข้อมูล post 
            ) 
        ,
        method="GET",action="/tour-results"
   )

@rt('/tour-results')
def get(tour_place:str, tour_id:str, tour_time:str): # ต้องประกาศ : str

    tours = website.SearchTour(tour_id,tour_place,tour_time)
    try:
        for tour in tours:
            print(tour.name)
    except:
        print("tours = 0")
        print(tour_place+"|"+tour_id+"|"+tour_time)

    if(tours!=None and tours!=[]):
        if(isinstance(tours,TourProgram)) :
            return Div(
            H2("ผลลัพธ์การค้นหา"),
            *[Card(H3(tours.id),P(tours.name), P(tours.place),P(tours.time)) ],
            Button("ย้อนกลับ", onclick="window.location.href='/'")  
            )
        else: 
            return Div(
            H2("ผลลัพธ์การค้นหา"),
            *[Card(H3(tour.id),P(tour.name), P(tour.place),P(tour.time)) for tour in tours],
            Button("ย้อนกลับ", onclick="window.location.href='/'")  
        )
    else:
        return Div(H2("ไม่พบผลลัพธ์"), Button("ย้อนกลับ", onclick="window.location.href='/'")  )



serve()
