#MainPage.py
from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

def register_routes(rt):
    @rt('/MainPage')
    def get():
        tour_list = website.tour_manager.get_all_tour()
        grouped_tours = [tour_list[i:i+3] for i in range(0, len(tour_list), 3)]
        
        return Div(Button("profile", onclick="location.href='/'"),
                   Button("article", onclick="location.href='/Article'"),
                   Button("Create Tour", onclick="location.href='/CreatTourPage'"),
                   Button("History"),
                   Button("Search", onclick="location.href='/search-tour'"),
                   Titled("MainPage",
                          Div(
                              *[Grid(*[Card(P(tour.name), P(tour.place),
                                    style="""
                                        transition: all 0.3s;
                                        cursor: pointer;
                                        margin-left : 40px;
                                        margin-right : 40px;
                                        padding: 30px
                                    """, 
                                    onmouseover="this.style.backgroundColor='#e0f7fa';this.style.transform='scale(1.03)';",
                                    onmouseout="this.style.backgroundColor='';this.style.transform='scale(1)';",
                        
                                    onclick = f"window.location.href='/tour-information/{tour.id}'"
                                    ) for tour in group]) for group in grouped_tours]
                          )
                   ))