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
                    P("วันที่เริ่มทัวร์"),
                    Label(Input(id="startDate", type="date", placeholder="วัน/เดือน/ปี",
                                style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),
                    P("วันที่จบทัวร์"),
                    Label(Input(id="endDate", type="date", placeholder="วัน/เดือน/ปี",
                                style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),
                    P("เลือกสถานที่ท่องเที่ยวที่แรก"),
                    Label(
                        Select(id="location",
                            *[Option(name, value=value) for value, name in locations] ,
                            style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;" # Loop to create options
                        )
                    ),
                    P("เลือกสถานที่ท่องเที่ยวที่ที่สอง"),
                    Label(
                        Select(id="location",
                            *[Option(name, value=value) for value, name in locations],
                            style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;"  # Loop to create options
                        )
                    ),

                    Button("ตกลง", type="button", hx_post="/CreateCustomizedTour",style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                ),style="background-color: #F5F7F8; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); max-width: 1200px; margin: 20px auto; text-align: center;"
            ))
        else:
            pending = website.pendingTour
            grouped_tours = [pending[i:i+3] for i in range(0, len(pending), 3)]
            return Div(Button("Back",onclick = "window.location.href='/MainPage'",style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
                        *[Grid(*[Card(H3(tour.name), 
                                      P(tour.place) ,
                                      Button("Confirm"),
                                      Button("Deny",hx_post=f"/denyTour?tourId={tour.id}")) for tour in group]) for group in grouped_tours]
                        )

    @rt('/CreateCustomizedTour', methods=["POST"])
    def post(startDate: str = None, endDate: str = None, location: str = None):
        if not startDate or not endDate or not location:
            return "Error: Missing required fields!", 400

        try:
            # Convert string dates to datetime objects
            start_date = datetime.strptime(startDate, "%Y-%m-%d")
            end_date = datetime.strptime(endDate, "%Y-%m-%d")

            # Validate the date order
            if start_date >= end_date:
                return "Error: Start date must be before end date!", 400

            # If valid, proceed with tour creation
            website.RequestCreateTour("test Tour",location)
            return Redirect("/MainPage")

        except ValueError:
            return "Error: Invalid date format!", 400  # Handles wrong date input

    @rt('/denyTour', methods=["POST"])
    def post(tourId : str):
        website.DenyTour(str(tourId))
        return Redirect('/CreatTourPage')
