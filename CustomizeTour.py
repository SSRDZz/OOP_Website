from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

locations = [
    ("bangkok", "กรุงเทพฯ"),
    ("phuket", "ภูเก็ต"),
    ("chiangmai", "เชียงใหม่"),
    ("pattaya", "พัทยา"),
    ("krabi", "กระบี่"),
]

def register_routes(rt):
    @rt('/CreatTourPage')
    def get():
        if(isinstance(website.currentUser,User)):
            return Div(Button("Back",onclick = "window.location.href='/MainPage'",
                              style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
                    Titled("ทัวร์แบบจัดเอง",
                    Form(
                    Card(
                        P("วันที่เริ่มทัวร์"),
                        Label(Input(id="startDate", type="date", placeholder="วัน/เดือน/ปี")),
                        P("วันที่จบทัวร์"),
                        Label(Input(id="endDate", type="date", placeholder="วัน/เดือน/ปี")),
                        P("เลือกสถานที่ท่องเที่ยวที่แรก"),
                        Label(
                            Select(id="location",
                                *[Option(name, value=value) for value, name in locations] # Loop to create options
                            )
                        ),
                        P("เลือกสถานที่ท่องเที่ยวที่ที่สอง"),
                        Label(
                            Select(id="location",
                                *[Option(name, value=value) for value, name in locations]  # Loop to create options
                            )
                        )
                    ),
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
                    ###
                    Button("ตกลง", type="button", hx_post="/CreateCustomizedTour",style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                ),style="background-color: #F5F7F8; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); max-width: 1200px; margin: 20px auto; text-align: center;"
            ))
        else:
            pending = website.pendingTour
            grouped_book = [pending[i:i+3] for i in range(0, len(pending), 3)]
            return Div(Button("Back",onclick = "window.location.href='/MainPage'",style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
                        *[Grid(*[Card(H3(book.tour_program.name), 
                                      P(book.tour_program.place) ,
                                      Button("Confirm",hx_post=f"/confirmTour?tourId={book.booking_id}"),
                                      Button("Deny",hx_post=f"/denyTour?tourId={book.booking_id}")) for book in group]) for group in grouped_book]
                        )

    @rt('/CreateCustomizedTour', methods=["POST"])
    def post(startDate: str, endDate: str, location: str,adult:str,child:str,fname:str,lname:str,email:str,phone:str):
        if (not startDate or not endDate or not location):
            return "Error: Missing required fields!", 400

        try:
            # Convert string dates to datetime objects
            start_date = datetime.strptime(startDate, "%Y-%m-%d")
            end_date = datetime.strptime(endDate, "%Y-%m-%d")

            # Validate the date order
            if start_date >= end_date:
                return "Error: Start date must be before end date!", 400
            
            if adult!="" and fname!="" and lname!="" and email!="" and phone!="":
                if(child=="" or child == None): child = "0"
                data_user = f"fname:{fname}|lname:{lname}|email:{email}|phone:{phone}|adult:{adult}|child:{child}"
                website.RequestCreateTour(fname+"'s Private Tour",location,data_user,f"{fname}",str(start_date)+" - "+str(start_date))
            return Redirect("/MainPage")

        except ValueError:
            return "Error: Invalid date format!", 400  # Handles wrong date input

    @rt('/denyTour', methods=["POST"])
    def post(tourId : str):
        website.DenyTour(str(tourId))
        return Redirect('/CreatTourPage')
    
    @rt('/confirmTour', methods=["POST"])
    def post(tourId : str):
        website.ConfirmTour(str(tourId))
        return Redirect('/CreatTourPage')
