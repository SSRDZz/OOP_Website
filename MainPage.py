from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

app, rt = fast_app()  # type: ignore

@rt('/')
def get():
    tour_list = website.tour_manager.get_all_tour()
    return Titled("MainPage",
                  Div(*[Card(P(result)) for result in results]))

serve()