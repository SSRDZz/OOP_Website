from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

def register_routes(rt):
    @rt('/MainPage')
    def get():
        user = website.currentUser
        tour_list = website.tour_manager.get_all_tour()
        grouped_tours = [tour_list[i:i+3] for i in range(0, len(tour_list), 3)]
        
        buttons = [
            Button("Profile", onclick="location.href='/'", style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
            Button("Article", onclick="location.href='/Article'", style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
            Button("Create Tour", onclick="location.href='/CreatTourPage'", style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
            Button("Search", onclick="location.href='/search-tour'", style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;")
        ]

        if isinstance(user, User):
            buttons.append(Button("History", onclick="location.href='/reserve-history'", style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"))

        return Div(
            Div(
                *buttons,
                style="margin-left: 60vw; padding: 1px 10px;"
            ),
            Titled("Tour Pro",
                Div(
                    Form(
                        H3("ค้นหาทัวร์สุดพิเศษ"),
                        Group(
                            Label(Input(id="tour_place", type="text", placeholder="ชื่อสถานที่")),
                            Label(Input(id="tour_id", type="text", placeholder="รหัสทัวร์")),
                            Label(Input(id="tour_time_go", type="date", placeholder="วันไป")),
                            Label(Input(id="tour_time_end", type="date", placeholder="วันกลับ")),
                            style="max-width: 75%; margin: 0 auto;"
                        ),
                        Button("Search", style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
                        method="GET", action="/tour-results",
                        style="margin-top: 20px; background-color: #F5F7F8; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); text-align: left;"
                    ),
                    style="margin: 20px;"
                ),
                Div(
                    *[
                        Grid(
                            *[
                                Card(
                                    P("ชื่อทัวร์ : " + tour.name),
                                    P("ปลายทาง : " + tour.place),
                                    style="""
                                        transition: all 0.3s;
                                        cursor: pointer;
                                        margin-left: 40px;
                                        margin-right: 40px;
                                        padding: 30px;
                                    """,
                                    onmouseover="this.style.backgroundColor='#FFFACD';this.style.transform='scale(1.03)';",
                                    onmouseout="this.style.backgroundColor='';this.style.transform='scale(1)';",
                                    onclick=f"window.location.href='/tour-information/{tour.id}'"
                                ) for tour in group
                            ]
                        ) for group in grouped_tours
                    ]
                )
            )
        )