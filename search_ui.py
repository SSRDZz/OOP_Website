from fasthtml.common import *
from dataclasses import dataclass
from BackEnd import *

# FastHTML app setup----------------------
app, rt = fast_app()

@rt('/')
def get():
   return Form(Group(H3("ค้นหาทัวร์สุดพิเศษ"),
                     
           Input(id="tour_place",placeholder="ชื่อสถานที่"),
           Input(id="tour_id",type="number",placeholder="รหัสทัวร์"),
           Input(id="tour_time",placeholder="วันที่"),
           
           Button("Search"),
           method="post",
           action = "/search-tour"
        )
   )

@rt('/search-tour')
def get(search:str):

    print(search) 
    # function search
    for tour in search:
        pass
    return Div(
        *[Card(H3(tour.id), P(tour.place))]
    )
   
serve()
