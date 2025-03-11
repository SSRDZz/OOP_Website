from fasthtml.common import *
from BackEnd import *

user = website.currentUser
selected_payment_method = "Credit/Debit"
payment_status = 'complete'
user_payment = None

def register_routes(rt):

    def updatePaymentMethod(method):
        global payment_status
        global selected_payment_method
        
        selected_payment_method = method
        if method in ["Credit/Debit", "PromptPay"]:
            payment_status = "complete"
        else:
            payment_status = "failed"

    @rt("/payment/{booking_id}/payment_complete/")
    def get(booking_id: str):
        global user_payment
        current_booked = user.search_booking(booking_id)
        user_payment.payment_method = selected_payment_method
        
        user_payment.Pay()
        
        page = Html(
            Head(
                Title("Payment Complete"),
                Style("""
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background-color: #fff;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }
                    .container h1 {
                        color: #4CAF50;
                        font-size: 36px;
                        margin-bottom: 20px;
                    }
                    .container p {
                        font-size: 18px;
                        margin-bottom: 30px;
                    }
                    .container a {
                        display: inline-block;
                        padding: 10px 20px;
                        color: #fff;
                        background-color: #4CAF50;
                        border-radius: 5px;
                        text-decoration: none;
                        transition: background-color 0.3s;
                    }
                    .container a:hover {
                        background-color: #45a049;
                    }
                """)
            ),
            Body(
                Div(
                    H1("Thank You!"),
                    P("Your payment has been successfully processed."),
                    A("Return to Home", href=f"/payment/{current_booked.booking_id}/update_status_done/"),
                    _class="container"
                )
            )
        )
        return page

    @rt("/payment/{booking_id}/payment_failed")
    def get():
        page = Html(
            Head(
                Title("Payment Failed"),
                Style("""
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background-color: #fff;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }
                    .container h1 {
                        color: #f44336;
                        font-size: 36px;
                        margin-bottom: 20px;
                    }
                    .container p {
                        font-size: 18px;
                        margin-bottom: 30px;
                    }
                    .container a {
                        display: inline-block;
                        padding: 10px 20px;
                        color: #fff;
                        background-color: #f44336;
                        border-radius: 5px;
                        text-decoration: none;
                        transition: background-color 0.3s;
                    }
                    .container a:hover {
                        background-color: #e53935;
                    }
                """)
            ),
            Body(
                Div(
                    H1("Payment Failed"),
                    P("Unfortunately, there was an issue processing your payment."),
                    A("Try Again", onclick = 'window.history.back()'),
                    _class="container"
                )
            )
        )
        return page

    def cdcardRender():
        page = Div(
            "Enter Credit/Debit Card Details",
            Br(), Br(),
            Label("Card Number:"),
            Br(),
            Input(id="card_number", type="text", placeholder="1234 5678 9012 3456", style="margin-bottom: 10px; padding: 5px; width: 100%;", oninput="formatCardNumber(this)"),
            Br(), Br(),
            Label("Expiry Date:"),
            Br(),
            Input(id="expiry_date", type="text", placeholder="MM/YY", style="margin-bottom: 10px; padding: 5px; width: 100%;", oninput="formatExpiryDate(this)"),
            Br(), Br(),
            Label("CVC:"),
            Br(),
            Input(id="cvc", type="text", placeholder="123", style="margin-bottom: 10px; padding: 5px; width: 100%;"),
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

    @rt("/payment/{booking_id}")
    def get(booking_id: str):  
        
        global payment_status
        global user_payment
        global user
        
        user = website.currentUser
        current_booked = user.search_booking(booking_id)
        user_payment = user.search_payment(booking_id)
        
        try:
            booking_data = current_booked.data.split('|')
        except AttributeError:
            booking_data = None
        
        if booking_data is not None:
                
            name = booking_data[0].split(':')[1] + " " +booking_data[1].split(':')[1] 
            email = booking_data[2].split(':')[1]
            phone = booking_data[3].split(':')[1]
            adults = int(booking_data[4].split(':')[1])
            children = int(booking_data[5].split(':')[1])
            discount = website.promotion.get_discount(current_booked.tour_program)

            
            total_price = user_payment.calculate_price(adults, children) - discount
            user_payment.net_price = total_price
            
        else:
            name = None
            email = None
            phone = None
            adults = None
            children = None
            total_price = 0
        
        page = Div(
            Head(
                Title("Payment Session"),
                Script("""
                    function validateCardForm() {
                        var cardNumber = document.getElementById('card_number').value;
                        var expiryDate = document.getElementById('expiry_date').value;
                        var cvc = document.getElementById('cvc').value;
                        
                        var cardNumberPattern = /^[0-9]{16}$/;
                        var expiryDatePattern = /^(0[1-9]|1[0-2])\/[0-9]{2}$/;
                        var cvcPattern = /^[0-9]{3}$/;
                        
                        if (!cardNumberPattern.test(cardNumber.replace(/\s+/g, ''))) {
                            alert('Invalid card number. Please enter a 16-digit card number.');
                            return false;
                        }
                        
                        if (!expiryDatePattern.test(expiryDate)) {
                            alert('Invalid expiry date. Please enter a valid expiry date in MM/YY format.');
                            return false;
                        }
                        
                        if (!cvcPattern.test(cvc)) {
                            alert('Invalid CVC. Please enter a 3-digit CVC.');
                            return false;
                        }
                        
                        return true;
                    }

                    function handlePayment(bookingId) {
                        var selectedMethod = document.querySelector('input[name="payment-method"]:checked').value;
                        if (selectedMethod === "Credit/Debit") {
                            if (validateCardForm()) {
                                location.href = '/payment/' + bookingId + '/payment_complete/';
                            }
                        } else if (selectedMethod === "PromptPay") {
                            location.href = '/payment/' + bookingId + '/payment_complete/';
                        } else {
                            location.href = '/payment/' + bookingId + '/payment_failed/';
                        }
                    }

                    function formatCardNumber(input) {
                        var value = input.value.replace(/\D/g, '').substring(0, 16);
                        var formattedValue = value.replace(/(.{4})/g, '$1 ').trim();
                        input.value = formattedValue;
                    }

                    function formatExpiryDate(input) {
                        var value = input.value.replace(/[^0-9]/g, '');
                        if (value.length >= 2) {
                            input.value = value.slice(0, 2) + '/' + value.slice(2, 4);
                        } else {
                            input.value = value;
                        }
                    }
                """)
            ),
            Body(
                Container(
                    Div(
                        Div("Tour Amateur", style="font-size: 30px; font-weight: bold; margin-top: 10px"),
                        Div(f"{user.username}", style="display: flex; align-items: center;"),
                        style="display: flex; justify-content: space-between;"
                    )   
                ),
                Div(
                    Div(
                        Div(
                            H3("Payment Method"),
                            Div(
                                Label(Input(type="radio", name="payment-method", value="Credit/Debit", checked=True, hx_post='/render-card'), "Credit/Debit"),
                                Label(Input(type="radio", name="payment-method", value="Bank Transfer", hx_post='/render-bank'), "Transfer from Bank"),
                                Label(Input(type="radio", name="payment-method", value="PromptPay", hx_post='/render-promptQR'), "PromptPay"),
                                method='post',
                                hx_target='#showed',
                            ),
                        ),
                        Div(
                            cdcardRender(),
                            selected_payment_method = "Credit/Debit",
                            id="showed"
                        ),
                        style="width:50%; margin-left : 20px"
                    ),
                    Div(
                        Div(
                            f"{current_booked.tour_program.name}",
                            style="background-color: #FFD700; padding: 10px; text-align: center; font-weight: bold; font-size: 18px"
                        ),
                        Div(
                            P(f"Location : {current_booked.tour_program.place}"),
                            P(f"Date : {current_booked.tour_program.time}"),
                            style="border: 1px solid #ccc; padding: 20px; margin-top: 20px;"
                        ),
                        Div(
                            P(f"Name: {name}"),
                            P(f"Email: {email}"),
                            P(f"Phone: {phone}"),
                            style="border: 1px solid #ccc; padding: 20px; margin-top: 20px;"
                        ),
                        Div(
                            P(f"Adults: {adults}"),
                            P(f"Children: {children}"),
                            P(f"Discount: {discount:,.2f}%"),
                            style="border: 1px solid #ccc; padding: 20px; margin-top: 20px;"
                        ),
                        Div(
                            f"Total Price: {total_price:,.2f} THB",
                            style="border: 1px solid #ccc; padding: 20px; margin-top: 20px; background-color: #333; color: white; font-weight: bold; font-size: 16px;"
                        ),
                        Div(
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
                                onclick=f"handlePayment('{booking_id}')",
                                onmouseover="this.style.backgroundColor='#ff8080';this.style.transform='scale(1.1)';",
                                onmouseout="this.style.backgroundColor='#ff0000';this.style.transform='scale(1)';"
                            ),
                            Button(
                                "Go Back",
                                style="""
                                background-color: #cccccc; 
                                color: black;
                                padding: 10px 20px;
                                text-align: center;
                                margin-top: 20px;
                                cursor: pointer;
                                transition: background-color 0.3s, transform 0.3s;
                                margin-left: 10px;
                                """,
                                id="go-back-button",
                                onclick="history.back()",
                                onmouseover="this.style.backgroundColor='#e0e0e0';this.style.transform='scale(1.1)';",
                                onmouseout="this.style.backgroundColor='#cccccc';this.style.transform='scale(1)';"
                            ),
                            style="display: flex; justify-content: space-between; margin-top: 20px;"
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