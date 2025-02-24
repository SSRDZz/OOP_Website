from fasthtml.common import *
from dataclasses import dataclass
from BackEnd import *

# FastHTML app setup----------------------
app, rt = fast_app()

@rt('/')
def get():
   return Form(H3("ค้นหาทัวร์สุดพิเศษ"),
            Group(
                     
                Input(id="tour_place",placeholder="ชื่อสถานที่"),
                Input(id="tour_id",type="number",placeholder="รหัสทัวร์"),
                Input(id="tour_time",placeholder="วันที่"),
                

                style="max-width: 75%; margin: 0 auto;"
                
                # 
        ),
        Button("Search",hx_post="/search-tour")
   )

@rt('/search-tour')
def post(tour_place,tour_id,tour_time):

    print(tour_place,tour_id,tour_time) 
    # function search
    for tour in search:
        pass
    return Div(
        *[Card(H3(tour.id), P(tour.place))]
    )
   
serve()
