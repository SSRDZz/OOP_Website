from fasthtml.common import *
from datetime import datetime
from BackEnd import *
import os
import json

# Constants
UPLOAD_FOLDER = "./Articleimage/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class Location:
    def __init__(self, name, description):
        self.__name = name
        self.__description = description
        self.__ratings = []

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.__ratings.append(rating)

    def get_average_rating(self):
        if not self.__ratings:
            return 0
        return sum(self.__ratings) / len(self.__ratings)

    def to_dict(self):
        return {
            "name": self.__name,
            "description": self.__description,
            "average_rating": self.get_average_rating()
        }

class Article:


    def __init__(self, title, href, image, description, content="", rating=0, locations=None):
        self.__title = title
        self.__href = href
        self.__image = image
        self.__description = description
        self.__content = content
        self.__rating = rating
        self.__locations = locations if locations else []

    @staticmethod
    def add_article(title, href, image_path, description, content, rating, locations=None):
        sanitized_href = href.lower().replace(" ", "-")
        new_article = Article(title, sanitized_href, image_path, description, content, rating, locations)
        website.articles.append(new_article)

    

    @staticmethod
    def find_article_by_href(href):
        href = href.lower()
        return next((article for article in website.articles if article.get_href() == href), None)

    def get_title(self):
        return self.__title

    def get_href(self):
        return self.__href

    def get_image(self):
        return self.__image

    def get_description(self):
        return self.__description

    def get_content(self):
        return self.__content

    def get_rating(self):
        return self.__rating

    def get_locations(self):
        return self.__locations

    def to_dict(self):
        return {
            "title": self.__title,
            "href": self.__href,
            "image": self.__image,
            "description": self.__description,
            "content": self.__content,
            "rating": self.__rating,
            "locations": [location.to_dict() for location in self.__locations]
        }

# Preload some articles
Article.add_article("Exploring the Alps", "alps", "/Articleimage/japan.jpg", "A thrilling adventure in the Alps!", "Details about the journey through the Alps...", 4)
Article.add_article("A Day in Paris", "paris", "/Articleimage/Paris.jpg", "Experience the beauty of Paris!", "A detailed guide to spending a day in Paris...", 5)


# Predefined locations
predefined_locations = [
    Location("Paris", "The capital city of France, known for its art, fashion, and culture."),
    Location("New York", "The largest city in the USA, known for its skyscrapers and cultural diversity."),
    Location("Tokyo", "The capital city of Japan, known for its modernity and traditional temples."),
    Location("Sydney", "The largest city in Australia, known for its Sydney Opera House and Harbour Bridge."),
    Location("Rome", "The capital city of Italy, known for its ancient history and architecture.")
]

def register_routes(rt):
    @rt('/Articleimage/<filename>')
    def get_uploaded_image(req, filename):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return P("File not found", style="color: red;")
        return FileResponse(file_path)

    @rt('/Article')
    def get():
        return Div(Titled("Article",
            Button(
                                "Go Back",
                                style="""
                                background-color: #FFD700; 
                                color: black;
                                padding: 10px 20px;
                                text-align: center;         
                                margin-top: 20px;
                                cursor: pointer;
                                transition: background-color 0.3s, transform 0.3s;
                                float: right;
                                """,
                                id="go-back-button",
                                onclick="history.back()",
                                onmouseover="this.style.backgroundColor='#FFD700';this.style.transform='scale(1.05)';",
                                onmouseout="this.style.backgroundColor='#FFD700';this.style.transform='scale(1)';",
                        ),
            Form(
                Input(
                    name="query",
                    placeholder="พิมพ์เพื่อค้นหา...",
                    hx_get="/search",
                    hx_trigger="keyup delay:500ms",
                    hx_target="#search-results"
                ),
                Div(id="search-results")
            ),
            (Form(
                H3("เพิ่มบทความใหม่"),
                Input(name="title", placeholder="Title"),
                Input(name="href", placeholder="URL"),
                Input(name="image", type="file"),
                Input(name="description", placeholder="Description"),
                Textarea(name="content", placeholder="Full Content"),
                Div(
                    Label("Select Locations: "),
                    Select(name="locations", multiple=True, size=5, style="margin-top: 10px; width: 100%;",*[Option(loc.get_name(),value=loc.get_name()) for loc in predefined_locations]),                    
                ),
                Button("Add Article", hx_post="/add_article", hx_encoding="multipart/form-data", onclick="redirectToSamePage()")
            ) if isinstance(website.currentUser, Staff) else None),
            Div(
                *[Div(
                    Card(
                        Img(src=article.get_image()),
                        H3(A(article.get_title(), href=f"/Article/{article.get_href()}", style="color: #1976d2;")),
                        P(article.get_description()),
                        
                        style="border: 2px solid #2196f3; border-radius: 10px; padding: 20px; margin: 10px;"
                    ),
                    style="width: 24%; display: inline-block; vertical-align: top;"
                ) for article in website.articles],
                id="article-list",
                style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;"
            ),
            Script("""
                function selectStarRating(starElement) {
                    var stars = document.querySelectorAll('.star');
                    var ratingInput = document.getElementById('rating-input');
                    var ratingValue = starElement.getAttribute('data-value');

                    stars.forEach(function(star) {
                        star.classList.remove('selected');
                    });

                    for (var i = 0; i < ratingValue; i++) {
                        stars[i].classList.add('selected');
                    }

                    ratingInput.value = ratingValue;
                }

                function redirectToSamePage() {{
                    setTimeout(function() {{
                        window.location.reload();
                    }}, 1000); // Adjust the delay as needed
                }}

                document.addEventListener('DOMContentLoaded', function () {
                    var starRatingDiv = document.getElementById('star-rating');
                    for (var i = 1; i <= 5; i++) {
                        var star = document.createElement('span');
                        star.classList.add('star');
                        star.setAttribute('data-value', i);
                        star.innerHTML = '★';
                        star.addEventListener('click', function() {
                            selectStarRating(this);
                        });
                        starRatingDiv.appendChild(star);
                    }
                });
            """),
            Style("""
                .star {
                    font-size: 2rem;
                    cursor: pointer;
                    color: #ccc;
                    transition: color 0.2s ease-in-out;
                }
                .star.selected {
                    color: gold;
                }
                select[multiple] {
                    width: 100%;
                    height: auto;
                    box-sizing: border-box;
                    overflow: hidden;
                }
                select[multiple] option {
                    display: block;
                    padding: 5px;
                    cursor: pointer;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }
                select[multiple] option:hover {
                    background-color: #f1f1f1;
                }
            """)
        ))

    @rt('/Article/{href}')
    def get(req, href: str):
        article = Article.find_article_by_href(href)
        if not article:
            return P("บทความไม่พบ", style="color: red;")

        return Titled(
            article.get_title(),
            Button(
                                "Go Back",
                                style="""
                                background-color: #FFD700; 
                                color: black;
                                padding: 10px 20px;
                                text-align: center;         
                                margin-top: 20px;
                                cursor: pointer;
                                transition: background-color 0.3s, transform 0.3s;
                                float: right;
                                """,
                                id="go-back-button",
                                onclick="history.back()",
                                onmouseover="this.style.backgroundColor='#FFD700';this.style.transform='scale(1.05)';",
                                onmouseout="this.style.backgroundColor='#FFD700';this.style.transform='scale(1)';",
                        ),
            Div(
                Img(src=article.get_image(), style="width: 70%; height: 75%; display: inline-block; vertical-align: top;"),
                style="text-align: center; margin-bottom: 20px;"
            ),
            Div(
                P(article.get_description(), style="font-weight: bold; margin-bottom: 20px;"),
                P(article.get_content(), style="line-height: 1.6;"),
            ),
            Div(
                H3("Locations"),
                *[Div(
                    H4(location.get_name()),
                    P(location.get_description()),
                    P(f"Average Rating: {location.get_average_rating():.2f} stars"),
                    Form(
                        Input(type="hidden", name="location_name", value=location.get_name()),
                        Div(
                            Label("Rate this location: "),
                            Div(id=f"location-star-rating-{location.get_name()}", style="display: flex; gap: 5px;"),
                            Input(type="hidden", name="location_rating", id=f"location-rating-input-{location.get_name()}"),
                            style="margin-top: 10px;"
                        ),
                        Button("Submit Rating", hx_post=f"/rate_location/{href}", hx_encoding="multipart/form-data", hx_target="this", hx_swap="outerHTML", onclick="redirectToSamePage()"),                    ),
                    style="border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin: 10px;"
                ) for location in article.get_locations()]
            ),
    
            Script(f"""
                function selectLocationStarRating(starElement, locationName) {{
                    var stars = document.querySelectorAll(`#location-star-rating-` + locationName + ` .star`);
                    var ratingInput = document.getElementById(`location-rating-input-` + locationName);
                    var ratingValue = starElement.getAttribute('data-value');
                    
                    // Reset all stars' color
                    stars.forEach(function(star) {{
                        star.style.color = '#ccc';  // Reset to default color
                        star.classList.remove('selected');
                    }});
            
                    // Highlight selected stars
                    for (var i = 0; i < ratingValue; i++) {{
                        stars[i].style.color = 'gold';  // Set selected color
                        stars[i].classList.add('selected');
                    }}
                    
                    // Set hidden input value
                    ratingInput.value = ratingValue;
                }}
                   
                function redirectToSamePage() {{
                    setTimeout(function() {{
                        window.location.reload();
                    }}, 1000); // Adjust the delay as needed
                }}

                document.addEventListener('DOMContentLoaded', function () {{
                    var locations = {json.dumps([location.get_name() for location in article.get_locations()])};
                    locations.forEach(function(locationName) {{
                        var starRatingDiv = document.getElementById(`location-star-rating-` + locationName);
                        for (var i = 1; i <= 5; i++) {{
                            var star = document.createElement('span');
                            star.classList.add('star');
                            star.setAttribute('data-value', i);
                            star.innerHTML = '★';
                            star.style.cursor = 'pointer';
                            star.style.fontSize = '24px';
                            star.style.color = '#ccc';  // Default star color
                            star.addEventListener('click', function() {{
                                selectLocationStarRating(this, locationName);
                            }});
                            starRatingDiv.appendChild(star);
                        }}
                    }});
                }});
            """),

    
            Style("""
                .star {
                    font-size: 2rem;
                    cursor: pointer;
                    color: #ccc;
                    transition: color 0.2s ease-in-out;
                }
                .star.selected {
                    color: gold;
                }
            """)
            ,
    
            style="padding: 20px; max-width: 800px; margin: auto;"
        )
    

    @rt('/search')
    def get(req):
        query = req.query_params.get("query", "").strip().lower()
        if not query:
            return P("กรุณากรอกข้อความค้นหา")
        matched_articles = [
            article for article in website.articles
            if query in article.get_title().lower() or query in article.get_description().lower()
        ]
        return Div(
            *[Div(
                Card(
                    Img(src=article.get_image()),
                    H3(A(article.get_title(), href=f"/article/{article.get_href()}", style="color: #1976d2;")),
                    P(article.get_description()),
                    P(f"Rating: {'★' * article.get_rating()}"),
                    style="border: 2px solid #2196f3; border-radius: 10px; padding: 20px; margin: 10px;"
                ),
                style="width: 24%; display: inline-block; vertical-align: top;"
            ) for article in matched_articles],
            style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;"
        ) if matched_articles else P(f"ไม่พบผลลัพธ์ที่เกี่ยวข้องกับ '{query}'")

    @rt('/add_article')
    async def post(req):
        form_data = await req.form()
        title = form_data.get("title", "").strip()
        href = form_data.get("href", "").strip()
        description = form_data.get("description", "").strip()
        content = form_data.get("content", "").strip()
        rating = form_data.get("rating", "0").strip()
        uploaded_image = form_data.get("image")
        selected_locations = [value for key, value in form_data.multi_items() if key == "locations"]

        if not uploaded_image or not hasattr(uploaded_image, "filename") or not uploaded_image.filename:
            return P("กรุณาอัปโหลดรูปภาพ", style="color: red;")

        image_filename = uploaded_image.filename
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        try:
            with open(image_path, "wb") as f:
                f.write(await uploaded_image.read())
            image_url = f"/Articleimage/{image_filename}"
            location_objects = [loc for loc in predefined_locations if loc.get_name() in selected_locations]
            Article.add_article(title, href, image_url, description, content, int(rating), location_objects)
            return P("บทความถูกเพิ่มแล้ว!", style="color: green;")
        except Exception as e:
            return P("เกิดข้อผิดพลาดในการบันทึกไฟล์", style="color: red;")

    @rt('/rate_location/{href}')
    async def post(req, href: str):
        form_data = await req.form()
        location_name = form_data.get("location_name", "").strip()
        location_rating = int(form_data.get("location_rating", 0))

        article = Article.find_article_by_href(href)
        if not article:
            return P("บทความไม่พบ", style="color: red;")

        location = next((loc for loc in article.get_locations() if loc.get_name() == location_name), None)
        if not location:
            return P("ไม่พบสถานที่", style="color: red;")

        location.add_rating(location_rating)
        return P("คะแนนถูกบันทึกแล้ว!", style="color: green;")

    @rt('/updates')
    def get():
        return Titled(
            "Updates",
            P("อัพเดตล่าสุด: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )