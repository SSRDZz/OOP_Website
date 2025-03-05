from fasthtml.common import *  # type: ignore
from LogIn import register_routes as register_login # type: ignore
from MainPage import register_routes as register_Main # type: ignore
from CustomizeTour import register_routes as register_CustomizeTour
from search_ui import register_routes as register_SearchUI
from Full_booking_UI import register_routes as register_BookUI
from Article import register_routes as register_ArticleUI
from ReserveHistory import register_routes as register_History_Payment_Ticket
app, rt = fast_app()  # type: ignore

register_login(rt)
register_SearchUI(rt)
register_Main(rt)
register_CustomizeTour(rt)
register_BookUI(rt)
register_ArticleUI(rt)
register_History_Payment_Ticket(rt)
                  
serve()

if __name__ == "__main__":
    print("Running MainPage.py directly")