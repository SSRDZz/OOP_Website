from fasthtml.common import *
from BackEnd import *
from datetime import datetime


def register_routes(rt):
    @rt('/search-tour')
    def get():
        return Div(Button("Home",onclick = "window.location.href='/MainPage'"),
                   Form(H3("ค้นหาทัวร์สุดพิเศษ"),
                Group(
                        
                    Label(Input(id="tour_place",type="text",placeholder="ชื่อสถานที่")),
                    Label(Input(id="tour_id",type="text",placeholder="รหัสทัวร์")),
                    Label(Input(id="tour_time_go",type="date",placeholder="วันไป")),
                    Label(Input(id="tour_time_end",type="date",placeholder="วันกลับ")),
                    # Label(),
                    

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
    def get(tour_place:str, tour_id:str, tour_time_go:str, tour_time_end:str): # ต้องประกาศ : str

        if(tour_time_go=="" and tour_time_end==""):
             tours = website.SearchTour(tour_id,tour_place,"")

        else:
            check = 0 # check ว่าใส่มากี่ค่า
            if(tour_time_go==""): 
                tour_time_go = "9999-12-31"
                check+=1
            if(tour_time_end==""): 
                tour_time_end = "1000-01-01"
                check+=1
            
            start = datetime.strptime(tour_time_go, '%Y-%m-%d')
            end = datetime.strptime(tour_time_end, '%Y-%m-%d')
            if start >= end and check == 0:
                    return Script(f"""
                            alert('Start date must be before end date!');
                            window.location.href='/search-tour';
                            """
                            )
            
            time = f"{start.day}/{start.month}/{start.year} - {end.day}/{end.month}/{end.year}"
            tours = website.SearchTour(tour_id,tour_place,time)
            

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
