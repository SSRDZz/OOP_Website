from fasthtml.common import *
from BackEnd import *

app, rt = fast_app()

selected_payment_method = "Credit/Debit"
payment_status = 'complete'

@dataclass
class Payment():    
    card_number = None
    expiry_date = None
    cvv = None
    bank_account_number = None
    promptpay_id = None


@rt("/payment_complete")
def get():
    print(payment_status)
    page = Html(
        Head(Title("Payment Complete")),
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
        Head(Title("Payment Failed")),
        Body(
            H1("Payment Failed"),
            P("Unfortunately, there was an issue processing your payment."),
            A("Try Again", href="/")
        )
    )
    
    return page


def cdcardRender():
    
    page = Div(
        "Enter Credit/Debit Card Details",
        Br(), Br(),
        Label("Card Number:"),
        Br(),
        Input(id="card_number", type="text", placeholder="1234 5678 9012 3456", style="margin-bottom: 10px; padding: 5px; width: 100%;"),
        Br(), Br(),
        Label("Expiry Date:"),
        Br(),
        Input(id="expiry_date", type="text", placeholder="MM/YY", style="margin-bottom: 10px; padding: 5px; width: 100%;"),
        Br(), Br(),
        Label("CVV:"),
        Br(),
        Input(id="cvv", type="text", placeholder="123", style="margin-bottom: 10px; padding: 5px; width: 100%;"),
        id="credit-details",
        style="border: 1px solid #ccc; padding: 20px; min-height: 150px; margin-top: 10px; background-color: #f9f9f9;"
    )
    return page


@rt('/render-card', methods=["POST"])
def post():
    updatePaymentMethod("Credit/Debit")
    return cdcardRender()


@rt('/render-bank', methods=["POST"])
def post():
    updatePaymentMethod("Bank Transfer")
    page = Div(
        H3("Bank Account Transfer Details"),
        Div(
            "Account Number: 123-456-789012",
            style="margin-top: 10px; font-size: 16px; font-weight: bold;"
        ),
        Div(
            "Bank Name: Sample Bank",
            style="margin-top: 10px; font-size: 16px;"
        ),
        id="bank-details",
        style="border: 1px solid #ccc; padding: 30px; width: 45%; margin-top: 20px;"
    )
    return page

@rt('/render-promptQR', methods=["POST"])
def post():
    updatePaymentMethod("PromptPay")
    page = Div(
        H3("PromptPay Details"),
        Div(
            Br(),
            Img(src="https://via.placeholder.com/300x300?text=PromptPay+QR", alt="PromptPay QR Code", style="margin-top: 10px;"),
        ),
        id="promptpay-details",
        style="border: 1px solid #ccc; padding: 35px; width: 45%; margin-top: 20px;"
    )
    return page


def updatePaymentMethod(method):
    global selected_payment_method
    global payment_status
    selected_payment_method = method
    payment_status = 'complete' if method == "Credit/Debit" else 'failed'
    print(payment_status)


@rt("/")
def get():
    global payment_status
    
    page = Div(
        Head(
            Title("Payment Session"),
        ),
        Body(
            Container(
                Div(
                    Div("Tour Amateur", style="font-size: 24px; font-weight: bold; margin-top: 10px"),
                    Div("Name", Img(src="user-icon.png", alt="User Icon"), style="display: flex; align-items: center; margin-right: 2%"),
                    style="display: flex; justify-content: space-between;"
                )
            ),
            Div(
                Div(
                   Div(
                        H3("Payment Method"),
                        Div(
                            Label(Input(type="radio", name="payment-method", checked=True, hx_post='/render-card'), "Credit/Debit"),
                            Label(Input(type="radio", name="payment-method", hx_post='/render-bank'), "Transfer from Bank"),
                            Label(Input(type="radio", name="payment-method", hx_post='/render-promptQR'), "PromptPay"),
                            method='post',
                            hx_target='#showed',
                        ),
                    ),
                    Div(
                        cdcardRender(),
                        id="showed"
                    ),
                    style="width:50%"
                ),
                Div(
                    Div(
                        "Tour Name",
                        style="background-color: #FFD700; padding: 10px; text-align: center; font-weight: bold; font-size: 18px"
                    ),
                    Div(
                        "ข้อมูล tour คร่าวๆ",
                        style="border: 1px solid #ccc; padding: 20px; margin-top: 20px;"
                    ),
                    Div(
                        "ราคา+โปรโมชั่น = ราคาสุทธิ",
                        style="border: 1px solid #ccc; padding: 20px; margin-top: 20px;"
                    ),
                    Button(
                        "ดำเนินการต่อ",
                        style="""
                        background-color: #ff0000; 
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        margin-top: 20px;
                        cursor: pointer;
                        transition: background-color 0.3s, transform 0.3s;
                        """,
                        id="payment-button",
                        
                        onclick=f"window.location.href = '/payment_complete'",

                        onmouseover="this.style.backgroundColor='#ff8080';this.style.transform='scale(1.1)';",
                        onmouseout="this.style.backgroundColor='#ff0000';this.style.transform='scale(1)';"
                    ),
                    style="padding: 20px; width: 45%;"
                ),
                style="display: flex; justify-content: space-between; margin-top: 20px;"
            ),
            style="font-family: Arial, sans-serif;"
        ),
        style="margin: 0;"
    )
    
    return page
serve()
                  