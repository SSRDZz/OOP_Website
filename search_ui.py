from fasthtml.common import *
from BackEnd import *
from datetime import datetime


def register_routes(rt):
    @rt('/search-tour')
    def get():
        return Div(
            # ปุ่ม Home
            Button("Home", onclick="window.location.href='/MainPage'", 
                   style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer;"),

            # ฟอร์มค้นหาทัวร์
            Form(
                H3("ค้นหาทัวร์สุดพิเศษ", 
                   style="color: #333; text-align: center; font-size: 24px; margin-bottom: 20px;"),

                Group(
                    Label(Input(id="tour_place", type="text", placeholder="ชื่อสถานที่",
                                style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),
                    Label(Input(id="tour_id", type="text", placeholder="รหัสทัวร์",
                                style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),
                    Label(Input(id="tour_time_go", type="date", placeholder="วันไป",
                                style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),
                    Label(Input(id="tour_time_end", type="date", placeholder="วันกลับ",
                                style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),

                    style="max-width: 400px; margin: 0 auto; display: flex; flex-direction: column; gap: 10px;"
                ),

                # ปุ่มค้นหา
                Button("Search", 
                       style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin-top: 20px;"),
                
                method="GET", action="/tour-results",
                style="background-color: #F5F7F8; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); max-width: 500px; margin: 20px auto; text-align: center;"
            ),
            
        # style = "background-color: #F5F7F8;"
        ),

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
            #     
            return Div(
                # หัวข้อหลัก
                H2("ผลลัพธ์การค้นหา", 
                style="color: #333; text-align: center; font-size: 28px; margin-bottom: 20px;"),
                
                # ใช้ Flexbox + Grid ช่วยจัดเรียงการ์ดให้ดูดี
                Div(
                    *[
                        Card(
                            H3(tour.id, style="color: #FFD700; font-size: 22px;"),  # ใช้สีเหลืองทอง
                            P(tour.name, style="color: #444; font-size: 18px; font-weight: bold;"),
                            P(f"สถานที่: {tour.place}", style="color: #666; font-size: 16px;"),
                            P(f"เวลาเดินทาง: {tour.time}", style="color: #666; font-size: 16px;"),
                            
                            # Style ของ Card
                            style="""
                                background-color: white;
                                border-radius: 10px;
                                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                                padding: 20px;
                                text-align: center;
                                transition: all 0.3s;
                                cursor: pointer;
                                width: 250px;
                            """,
                            
                            # Hover Effect
                            onmouseover="this.style.backgroundColor='#FFFACD';this.style.transform='scale(1.05)';",
                            onmouseout="this.style.backgroundColor='white';this.style.transform='scale(1)';",
                            
                            # คลิกเพื่อดูรายละเอียด
                            onclick=f"window.location.href='/tour-information/{tour.id}'"
                        ) for tour in tours
                    ],
                    
                    # Grid Layout ให้การ์ดเรียงสวย
                    style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px;"
                ),
                
                # ปุ่มย้อนกลับ
                Button("ย้อนกลับ", onclick="window.history.back()", 
                    style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin-top: 20px; display: block; margin-left: auto; margin-right: auto;"),
                
                style="margin: 20px;"
            )
        
        else:
            return Script(f"""
                          alert('ไม่พบผลลัพธ์');
                          window.location.href='/search-tour';
                          """
                          )
