#MainPage.py
from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

def register_routes(rt):
    @rt('/MainPage')
    def get():
        tour_list = website.tour_manager.get_all_tour()
        grouped_tours = [tour_list[i:i+3] for i in range(0, len(tour_list), 3)]
        
        return Div(Button("profile", onclick="location.href='/SignUpPage'"),
                   Button("article"),
                   Button("Create Tour", onclick="location.href='/CreatTourPage'"),
                   Titled("MainPage",
                          Div(
                              *[Grid(*[Card(P(tour.name), P(tour.place)) for tour in group]) for group in grouped_tours]
                          )
                   ))