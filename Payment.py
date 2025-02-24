from fasthtml.common import *
from BackEnd import *

app, rt = fast_app()
payment_status = False

@dataclass
class Payment():
    card_number = None
    expiry_date = None
    cvv = None
    bank_account_number = None
    promptpay_id = None

@rt("/")
def get():
    page = Html(
        Head(
            Title("Payment Session"),
            Script("""
                function showPaymentDetails(paymentMethod) {
                    document.getElementById('credit-details').style.display = paymentMethod === 'credit' ? 'block' : 'none';
                    document.getElementById('bank-details').style.display = paymentMethod === 'bank' ? 'block' : 'none';
                    document.getElementById('promptpay-details').style.display = paymentMethod === 'promptpay' ? 'block' : 'none';
                }

                document.addEventListener("DOMContentLoaded", function() {
                    document.querySelector('input[name="payment-method"][value="credit"]').checked = true;
                    showPaymentDetails('credit'); // Default to Credit/Debit details being shown

                    // Check the selected payment method on button click
                    const paymentButton = document.getElementById('payment-button');
                    paymentButton.addEventListener('click', function(event) {
                        const selectedPaymentMethod = document.querySelector('input[name="payment-method"]:checked').value;

                        if (selectedPaymentMethod === 'bank' || selectedPaymentMethod === 'promptpay') {
                            // Simulate successful payment
                            window.location.href = '/payment_complete';
                        } else {
                            // Simulate failed payment for Credit/Debit
                            window.location.href = '/payment_failed';
                        }
                    });
                });
            """)

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
                    H3("Payment Method"),
                    Div(
                        Label(Input(type="radio", name="payment-method", value="credit", onclick="showPaymentDetails('credit')", checked=true), "Credit/Debit"),
                        Label(Input(type="radio", name="payment-method", value="bank", onclick="showPaymentDetails('bank')"), "Transfer from Bank"),
                        Label(Input(type="radio", name="payment-method", value="promptpay", onclick="showPaymentDetails('promptpay')"), "PromptPay"),
                    ),
                    
                    Div(
                        "Enter Credit/Debit Card Details",
                        Br(), Br(),
                        Label("Card Number:"),
                        Br(),
                        Input(id="card_number" ,type="text", placeholder="1234 5678 9012 3456", style="margin-bottom: 10px; padding: 5px; width: 100%;"),
                        Br(), Br(),
                        Label("Expiry Date:"),
                        Br(),
                        Input(id="expiry_date", type="text", placeholder="MM/YY", style="margin-bottom: 10px; padding: 5px; width: 100%;"),
                        Br(), Br(),
                        Label("CVV:"),
                        Br(),
                        Input(id="cvv", type="text", placeholder="123", style="margin-bottom: 10px; padding: 5px; width: 100%;"),
                        id="credit-details",
                        style="display: none; border: 1px solid #ccc; padding: 20px; min-height: 150px; margin-top: 10px; background-color: #f9f9f9;"
                    ),
                    
                    Div(
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
                        style="display: none;border: 1px solid #ccc; padding: 30px; width: 45%; margin-top: 20px;"
                    ),
                    
                    Div(
                        H3("PromptPay Details"),
                        Div(
                            Br(),
                            Img(src="https://via.placeholder.com/300x300?text=PromptPay+QR", alt="PromptPay QR Code", style="margin-top: 10px;"),
                           
                        ),
                        id="promptpay-details",
                        style="display: none;border: 1px solid #ccc; padding: 35px; width: 45%; margin-top: 20px;"
                    ),
                    
                    style="border: 1px solid #ccc; padding: 35px; width: 45%;"
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
                        onclick=f"window.location.href = '{'/payment_complete' if payment_status else '/payment_failed'}'",
                        onmouseover="this.style.backgroundColor='#ff8080';this.style.transform='scale(1.1)';",
                        onmouseout="this.style.backgroundColor='#ff0000';this.style.transform='scale(1)';"
                    ),
                    style="padding: 20px; width: 45%;"
                ),
                
                style="display: flex; justify-content: space-between; margin-top: 20px;"
            ),
            
            
            
            
            style="font-family: Arial, sans-serif;"
        )
    )
    
    return page

@rt("/payment_complete")
def get():
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

serve()
