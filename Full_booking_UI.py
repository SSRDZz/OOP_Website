from fasthtml.common import *
from BackEnd import *

def register_routes(rt):
    @rt('/tour-information/{tour_id}') # tour-description
    def get(tour_id:str):

        # tour_id = 1
        tour = website.SearchTour(id=tour_id)

        return Head(Title("Tour ame"),
            Body(
                    Div(
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

                                Label("เด็ก 2xx บาท"),
   
                            ),
                            style="margin-bottom: 20px; margin-right:60px"
                        ),
                    
                    style="display: flex; flex-direction: column; gap: 20px; width: 1200px;",
                    
                ),
                style="display: flex; flex-direction: row; gap: 20px; margin: 20px;width:100%;"
            ),
        )
    )   

    @rt('/tour-book/{tour_id}') 
    def get(tour_id:str):
        tour = website.SearchTour(id=tour_id)

        return Head(Title("Tour ame"),
            Body(
                    Div(
                        
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
                                Input(id="adult",type="number",min="0",max="100",placeholder="จำนวน"),
                                Br(),
                                # เด็ก
                                Label("เด็ก 2xx บาท"),
                                Input(id="child",type="number",min="0",max="100",placeholder="จำนวน"),
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
                                Input(type="text",id="fname", placeholder="ชื่อ"),
                                style="margin-bottom: 5px;"
                            ),
                            Div(
                                Label("นามสกุล: "),
                                Input(type="text",id="lname", placeholder="นามสกุล"),
                                style="margin-bottom: 5px;"
                            ),
                            Div(
                                Label("อีเมล: "),
                                Input(type="email",id="email", placeholder="อีเมล"),
                                style="margin-bottom: 5px;"
                            ),
                            Div(
                                Label("มือถือ: "),
                                Input(type="text",id="phone", placeholder="เบอร์มือถือ"),
                                style="margin-bottom: 5px;"
                            ),
                            style="padding: 10px;"
                        ),
                    # ปุ่มยืนยัน
                    Button("ยืนยันการจอง",style="width: 150px; margin-top: 10px;"),
                    method="GET",action=f"/tour-book-result/{tour_id}", #f"location.href='/tour-book/{tour_id}'
                    style="display: flex; flex-direction: column; gap: 20px; width: 1200px;",
                    
                ),
                style="display: flex; flex-direction: row; gap: 20px; margin: 20px;"
            )
        )
    )   

    @rt('/tour-book-result/{tour_id}')
    def get(adult:str,child:str,fname:str,lname:str,email:str,phone:str,tour_id:str):
        # print("min")
        if adult!="" and fname!="" and lname!="" and email!="" and phone!="":
            if(child=="" or child == None): child = "0"
            data_user = f"fname:{fname}|lname:{lname}|email:{email}|phone:{phone}|adult:{adult}|child:{child}"
            # print(data_user)
            id = f"{tour_id}_{fname}"
            website.booking_tour(website.SearchTour(id=tour_id), data_user, id)
            return Script(f"""
                          alert('Success');
                          window.location.href='/MainPage';
                          """
                          )
        else :
            return Script(f"""
                          alert('Please Input again');
                          window.location.href='/tour-book/{tour_id}';
                          """
                          )
           
