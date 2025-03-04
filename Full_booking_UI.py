from fasthtml.common import *
from BackEnd import *

app, rt = fast_app()

@rt('/') # tour-description
def get():

    tour_id = 1
    tour = website.SearchTour(id=tour_id)

    return Head(Title("Tour ame"),
           Body(
                Container(
                    Div(
                        Div(
                        H2("รายละเอียดทัวร์",style = "text-align:center"),
                        
                        Img(src = "https://cdn.weon.website/WOW/8546/ImageProduct/tpro221122.png?v=2",
                            style = "width:100%; height: auto ; margin-top:20px ; margin-bottom:20px"), # picture ,
                       Div(
                        Div(
                                P(f"ชื่อทัวร์ : {tour.name}")
                            ),
                            Div(
                                P(f"รหัสทัวร์ : {tour.id}")
                            ),
                            Div(
                                P(f"สถานที่ : {tour.place}")
                            ),
                            Div(
                                P(f"วันที่ : {tour.time}")
                            ),
                            style = "text-align:left " # ; margin-top:20px
                        )
                       ,

                        style="width:350px"
                    ),
                        # ปุ่มจองทัวร์
                    Button("จองทัวร์",style="width: 150px; margin-top: 10px;", onclick=f"location.href='/tour-book/{tour_id}'"),
                    # method="GET",action="/tour-book",
                    style = "margin-right:20px ; text-align:center " 
                    )
                ,
                Div(
                    # กล่องแรก: รายละเอียด
                    Card(
                        H4("รายละเอียด"),
                        Div(
                            # ผู้ใหญ่
                            Label("ผู้ใหญ่ 8xx บาท"),
                            # Input(id="adult",type="number",placeholder="จำนวน"),
                            # Br(),
                            # # เด็ก
                            Label("เด็ก 2xx บาท"),
                            # Input(id="child",type="number",placeholder="จำนวน"),
                            # Br(),
                            # # ราคารวม
                            # P("รวม: 1xxx บาท"),
                            # style="margin: 10px 0;"
                        ),
                        style="margin-bottom: 20px;"
                    ),
                
                style="display: flex; flex-direction: column; gap: 20px; width: 1200px;",
                
            ),
            style="display: flex; flex-direction: row; gap: 20px; margin: 20px;"
        )
    )
)   

@rt('/tour-book/{tour_id}') 
def get(tour_id:str):
    tour = website.SearchTour(tour_id)

    return Head(Title("Tour ame"),
           Body(
                Container(
                    
                    Div(
                    Card(
                        H2("รายละเอียดทัวร์",style = "text-align:center"),
                        
                        Img(src = "https://cdn.weon.website/WOW/8546/ImageProduct/tpro221122.png?v=2",
                            style = "width:100%; height: auto"), # picture ,
                       
                       Div(
                            P(f"ชื่อทัวร์ : {tour.name}")
                        ),
                        Div(
                            P(f"รหัสทัวร์ : {tour.id}")
                        ),
                        Div(
                            P(f"สถานที่ : {tour.place}")
                        ),
                        Div(
                            P(f"วันที่ : {tour.time}")
                        ),

                        style="width:350px"
                        ),
                    style = "margin-right :20px"
                    )
                ,
                Form(
                    # กล่องแรก: จำนวนผู้เดินทาง
                    Card(
                        H3("จำนวนผู้เดินทาง"),
                        Div(
                            # ผู้ใหญ่
                            Label("ผู้ใหญ่ 8xx บาท"),
                            Input(id="adult",type="number",placeholder="จำนวน"),
                            Br(),
                            # เด็ก
                            Label("เด็ก 2xx บาท"),
                            Input(id="child",type="number",placeholder="จำนวน"),
                            Br(),
                            # ราคารวม
                            P("รวม: 1xxx บาท"),
                            style="margin: 10px 0;"
                        ),
                        style="margin-bottom: 20px;"
                    ),

                    # กล่องสอง: ข้อมูลผู้เดินทาง
                    Card(
                        H3("ข้อมูลผู้เดินทาง"),
                        Div(
                            Label("ชื่อ: "),
                            Input(id="fname", placeholder="ชื่อ"),
                            style="margin-bottom: 5px;"
                        ),
                        Div(
                            Label("นามสกุล: "),
                            Input(id="lname", placeholder="นามสกุล"),
                            style="margin-bottom: 5px;"
                        ),
                        Div(
                            Label("อีเมล: "),
                            Input(id="email", placeholder="อีเมล"),
                            style="margin-bottom: 5px;"
                        ),
                        Div(
                            Label("มือถือ: "),
                            Input(id="phone", placeholder="เบอร์มือถือ"),
                            style="margin-bottom: 5px;"
                        ),
                        style="padding: 10px;"
                    ),
                # ปุ่มยืนยัน
                Button("ยืนยันการจอง",style="width: 150px; margin-top: 10px;"),
                method="GET",action="/tour-book-result",
                style="display: flex; flex-direction: column; gap: 20px; width: 1200px;",
                
            ),
            style="display: flex; flex-direction: row; gap: 20px; margin: 20px;"
        )
    )
)   

@rt('/tour-book-result')
def get(adult:str,child:str,fname:str,lname:str,email:str,phone:str,tour_id:str):
    # print("min")
    if (child=="" or int(child)>=0) and adult!="" :
        if (0<int(adult)<100):
            data_user = f"fname:{fname}|lname:{lname}|email:{email}|phone:{phone}"
            website.booking_tour(website.SearchTour(tour_id), data_user)
            return Div(
                    H2("Success"),
                    Button("ย้อนกลับ", onclick="window.location.href='/'")  
            )
    else :
        return Div(
                H1("Something don't work normal"),
                Button("ย้อนกลับ", onclick="window.location.href='/'")  
        )
    
serve()