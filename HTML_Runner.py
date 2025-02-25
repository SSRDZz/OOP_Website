from fasthtml.common import *  # type: ignore
from LogIn import register_routes as register_login # type: ignore
from MainPage import register_routes as register_Main # type: ignore

app, rt = fast_app()  # type: ignore

register_login(rt)
register_Main(rt)
                  
serve()