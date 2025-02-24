from fasthtml.common import * # type: ignore
from datetime import datetime
from BackEnd import *# type: ignore

app, rt = fast_app() # type: ignore

@rt('/')
def get():
    return Titled("ทัวร์แบบจัดเอง",
        Form(#ช่องพิมพ์ # type: ignore
            P("วันที่เริ่มทัวร์"),
            Label(Input(id="startDate",placeholder="วัน/เดือน/ปี")),
            P("วันที่จบทัวร์"),
            Label(Input(id="endDate",placeholder="วัน/เดือน/ปี")),
            P("เลือกสถานที่ท่องเที่ยว"),
            Label(Input(id="location",placeholder="ไปเที่ยวไหนดี...")),

            Button("ตกลง",type="submit",hx_post="/CreateCustomizedTour"),
        ))

@rt('/CreateCustomizedTour')
def post(startDate,endDate,location):
    if(location != None and startDate != None and endDate != None):
        website.RequestCreateTour(str(location))
    
serve()