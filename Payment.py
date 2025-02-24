from fasthtml.common import *
from dataclasses import dataclass

app, rt = fast_app()

@rt("/")
def get():
    return Titled(
        "Payment Session",
        Container(
            Div(  
                Div("Web Name",style=" font-size: 24px;font-weight: bold;"),
                Div("Name", Img(src="user-icon.png"), alt="User Icon",style=" display: flex; align-items: center;"),
                style="display: flex;justify-content: space-between;",
            ),
            Div(
                Div(
                    H3("Payment Method"),
                    Div(    
                        
                        Label(Input(type="radio", name="payment-method"), "Credit/Debit"),
                        Label(Input(type="radio", name="payment-method"), "Transfer from Bank"),
                        Label(Input(type="radio", name="payment-method"), "Promptpay"),
                        
                    ),
                    
                    Div(
                        "Detail",
                        Div(style="border: 1px solid #ccc; padding: 50px;")
                    ),
                    
                    style="border: 1px solid #ccc; padding: 20px; width: 45%;"
                ),
                
                Div(
                    Div(
                        "Tour Name",
                        
                        Style="""
                        background-color: #FFD700;
                        padding: 10px;
                        text-align: center;
                        font-weight: bold;
                        font-size : 18px
                        """
                    ),
                    Div(
                        
                        "ข้อมูล tour คร่าวๆ",
                        
                        style="""
                        border: 1px solid #ccc;
                        padding: 20px;
                        margin-top: 20px;
                        
                        """
                        
                    ),
                    Div(
                        
                        "ราคา+โปรโมชั่น = ราคาสุทธิ",

                        style="""
                        border: 1px solid #ccc;
                        padding: 20px;
                        margin-top: 20px;
                        
                        """
                    ),
                    
                    Button(
                        "ดำเนินการต่อ",
                        onclick="",               
                        style="""
                        background-color: #FF4500; 
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        margin-top: 20px;
                        cursor: pointer;
                        """  
                    ),
                
                    style="""
                    border: 1px solid #ccc;
                    padding: 20px;
                    width: 45%;
                    """
                ),
                
                
                style="""
                display: flex;
                justify-content: space-between;
                margin-top: 20px;"""
            )
        )
    )

serve()

