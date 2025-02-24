from fasthtml.common import * ##
from dataclasses import dataclass
from BackEnd import *

app, rt = fast_app()

payment = False

@rt("/")
def get():
    page = Html(
        Head(
            Title("Payment Session")    
        ),

        Body(
            Container(
                Div(  
                    Div("Web Name", style=" font-size: 24px;font-weight: bold; margin-top: 10px"),
                    Div("Name", Img(src="user-icon.png"), alt="User Icon", style=" display: flex; align-items: center; margin-right: 2%"),
                    style="display: flex;justify-content: space-between;",
                )
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
                        Div(style="border: 1px solid #ccc; padding: 35%;"),
                        style="margin-top: 10px"
                    ),
                    
                    style="border: 1px solid #ccc; padding: 35px; width: 45%;"
                ),
                
                Div(
                    Div(
                        "Tour Name",
                        
                        style="""
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
                        onclick=f"window.location.href = '{'/payment_complete' if payment else '/payment_failed'}'",
                        style="""
                        background-color: #ff0000; 
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        margin-top: 20px;
                        cursor: pointer;
                        transition: background-color 0.3s, transform 0.3s;
                        """,
                        onmouseover="this.style.backgroundColor='#ff8080';this.style.transform='scale(1.1)';",
                        onmouseout="this.style.backgroundColor='#ff0000';this.style.transform='scale(1)';"  
                    ),
                
                    style="""
                    padding: 20px;
                    width: 45%;
                    """
                ),
                
                style="""
                display: flex;
                justify-content: space-between;
                margin-top: 20px;"""
            ),
           
           style= "font-family: Arial, sans-serif;" 
        )
    )
    
    return page


@rt("/payment_complete")
def get():
    page = Html(
        Head(
            Title("Payment Complete")
        ),
        Body(
            H1("Thank You!"),
            P("Your payment has been successfully processed."),
            A("Return to Home", href="/")
        )
    )
    
    return page

@rt("/payment_failed")
def get():
    page = Html(
        Head(
            Title("Payment Failed")
        ),
        Body(
            H1("Payment Failed"),
            P("Unfortunately, there was an issue processing your payment."),
            A("Try Again", href="/")
        )
    )
    
    return page



serve()