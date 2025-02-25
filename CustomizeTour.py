from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

app, rt = fast_app()  # type: ignore
locations = [
    ("bangkok", "กรุงเทพฯ"),
    ("phuket", "ภูเก็ต"),
    ("chiangmai", "เชียงใหม่"),
    ("pattaya", "พัทยา"),
    ("krabi", "กระบี่"),
]

@rt('/')
def get():
    return Titled("ทัวร์แบบจัดเอง",
        Form(
            P("วันที่เริ่มทัวร์"),
            Label(Input(id="startDate", type="date", placeholder="วัน/เดือน/ปี")),
            P("วันที่จบทัวร์"),
            Label(Input(id="endDate", type="date", placeholder="วัน/เดือน/ปี")),
            P("เลือกสถานที่ท่องเที่ยวที่แรก"),
            Label(
                Select(id="location",
                    *[Option(name, value=value) for value, name in locations]  # Loop to create options
                )
            ),
            P("เลือกสถานที่ท่องเที่ยวที่ที่สอง"),
            Label(
                Select(id="location",
                    *[Option(name, value=value) for value, name in locations]  # Loop to create options
                )
            ),

            Button("ตกลง", type="button", hx_post="/CreateCustomizedTour"),
            method="post",
            onkeydown="if(event.key==='Enter'){event.preventDefault();}"
        )
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
        return "Tour created successfully!"

    except ValueError:
        return "Error: Invalid date format!", 400  # Handles wrong date input

serve()
