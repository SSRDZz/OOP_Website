#MainPage.py
from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

def register_routes(rt):
    @rt('/MainPage')
    def get():
        tour_list = website.tour_manager.get_all_tour()
        return Div(Button("profile",onclick="location.href='/SignUpPage'"),
                    Button("article"),
                    Titled("MainPage",
                        Grid(*[Card(P(tour.name),P(tour.place)) for tour in tour_list])),
                    )