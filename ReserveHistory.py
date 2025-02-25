from fasthtml.common import *
from BackEnd import *

app, rt = fast_app()


def renderHistory():
    return  Body(
                  
                Card( 
                    Grid(
                        Div("Example Tour"),  
                        Div("2025-02-25"),  
                        Div("(pending, ปุ่มชำระเงิน, success)"),  
                        Div(Button("พิมพ์ตั๋ว",hx_post="")),  
                        Div(Button("ยกเลิก", ),  
                        style="display: grid; grid-template-columns: repeat(5, 2fr); text-align: center; "
                        ),
                    ),
                    style="padding: 10px; margin: 5px; border: 1px solid #ddd;  align-items: center;"
                )
            )





@rt('/')
def get():
    page = Div(
        Head(
            Title("Tour Amateur"),
            style="""
            
            """ 
        ),
        Div(
            H1("Web Name"),
            P("ประวัติการจอง"),
        ),
        Grid(
            Card("Tour"),
            Card("Date"),
            Card("Status"),
            Card("พิมพ์ตั๋ว"),
            Card("ยกเลิกการจอง"),
            style="text-align: center;"
        ),

        renderHistory(),
        renderHistory(),
        renderHistory(),
        renderHistory(),
        
        
        style="margin: 15px;"
    )
    return page

serve()
