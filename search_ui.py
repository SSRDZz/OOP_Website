from fasthtml.common import *
from BackEnd import *

def register_routes(rt):
    @rt('/search-tour')
    def get():
        return Div(Button("Home",onclick = "window.location.href='/MainPage'"),
                   Form(H3("ค้นหาทัวร์สุดพิเศษ"),
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
            ))

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
                return Div(
                H2("ผลลัพธ์การค้นหา"),
                *[Card(H3(tour.id),P(tour.name), P(tour.place),P(tour.time),
                style="""
                    transition: all 0.3s;
                    cursor: pointer;
                    margin-left : 40px;
                    margin-right : 40px;
                    padding: 30px
                """, 
                onmouseover="this.style.backgroundColor='#e0f7fa';this.style.transform='scale(1.03)';",
                onmouseout="this.style.backgroundColor='';this.style.transform='scale(1)';",

                onclick = f"window.location.href='/tour-information/{tour.id}'") for tour in tours],
                
                Button("ย้อนกลับ", onclick="window.location.href='/search-tour'")  ,
                style = """
                    margin : 20px;
                    
                """
            )
        else:
            return Script(f"""
                          alert('ไม่พบผลลัพธ์');
                          window.location.href='/search-tour';
                          """
                          )
