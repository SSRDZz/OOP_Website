from fasthtml.common import *  # type: ignore
from LogIn import register_routes as register_login # type: ignore
from MainPage import register_routes as register_Main # type: ignore
from CustomizeTour import register_routes as register_CustomizeTour
from search_ui import register_routes as register_SearchUI

app, rt = fast_app()  # type: ignore

register_login(rt)
register_Main(rt)
register_CustomizeTour(rt)
register_SearchUI(rt)
                  
serve()

if __name__ == "__main__":
    print("Running MainPage.py directly")