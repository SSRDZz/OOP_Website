from fasthtml.common import *
from BackEnd import *

app, rt = fast_app()

@rt('/')
def get():
    tour = website.SearchTour(id=1)

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
                method="GET",action="/tour-book",
                style="display: flex; flex-direction: column; gap: 20px; width: 1200px;",
                
            ),
            style="display: flex; flex-direction: row; gap: 20px; margin: 20px;"
        )
    )
)   

@rt('/tour-book')
def get(adult:str,child:str,fname:str,lname:str,email:str,phone:str):
    print("min")
    if (child=="" or int(child)>=0) and adult!="" :
        if (0<int(adult)<100):
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