from fasthtml.common import *
from datetime import datetime
from BackEnd import *
import os

# Encapsulate constants
__UPLOAD_FOLDER = "./Articleimage/"
os.makedirs(__UPLOAD_FOLDER, exist_ok=True)

# Preload some articles
Article.add_article("Exploring the Alps", "alps", "/Articleimage/japan.jpg", "A thrilling adventure in the Alps!", "Details about the journey through the Alps...", 4)
Article.add_article("A Day in Paris", "paris", "/Articleimage/Paris.jpg", "Experience the beauty of Paris!", "A detailed guide to spending a day in Paris...", 5)

def register_routes(rt):
    @rt('/Articleimage/<filename>')
    def get_uploaded_image(req, filename):
        file_path = os.path.join(__UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return P("File not found", style="color: red;")
        return FileResponse(file_path)

    @rt('/Article')
    def get():
        return Titled("Article",
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
                    Label("Star Rating: "),
                    Div(id="star-rating", style="display: flex;"),
                    Input(type="hidden", name="rating", id="rating-input"),
                    style="margin-top: 10px;"
                ),
                Button("Add Article", hx_post="/add_article", hx_encoding="multipart/form-data")
            ) if isinstance(website.currentUser, Staff) else None),
            Div(
                *[
                    Div(
                        Card(
                            Img(src=article.get_image()),
                            H3(A(article.get_title(), href=f"/Article/{article.get_href()}", style="color: #1976d2;")),
                            P(article.get_description()),
                            P(f"Rating: {'★' * article.get_rating()}"),
                            style="border: 2px solid #2196f3; border-radius: 10px; padding: 20px; margin: 10px;"
                        ),
                        style="width: 24%; display: inline-block; vertical-align: top;"
                    )
                    for article in Article.get_articles()
                ],
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
            """)
        )

    @rt('/Article/{href}')
    def get(req, href: str):
        """ Display full article details """
        article = Article.find_article_by_href(href)

        if not article:
            return P("บทความไม่พบ", style="color: red;")

        return Titled(
            article.get_title(),
            Div(
                Img(src=article.get_image(), style="width: 70%; height: 75%; display: inline-block; vertical-align: top;"),
                style="text-align: center; margin-bottom: 20px;"
            ),
            Div(
                P(article.get_description(), style="font-weight: bold; margin-bottom: 20px;"),
                P(article.get_content(), style="line-height: 1.6;"),
                P(f"Rating: {'★' * article.get_rating()} ({article.get_rating()} stars)", style="font-size: 1.2em; color: #ff9800;")
            ),
            style="padding: 20px; max-width: 800px; margin: auto;"
        )

    @rt('/search')
    def get(req):
        query = req.query_params.get("query", "").strip().lower()
        if not query:
            return P("กรุณากรอกข้อความค้นหา")
        matched_articles = [
            article for article in Article.get_articles()
            if query in article.get_title().lower() or query in article.get_description().lower()
        ]
        return Div(
            *[
                Div(
                    Card(
                        Img(src=article.get_image()),
                        H3(A(article.get_title(), href=f"/article/{article.get_href()}", style="color: #1976d2;")),
                        P(article.get_description()),
                        P(f"Rating: {'★' * article.get_rating()}"),
                        style="border: 2px solid #2196f3; border-radius: 10px; padding: 20px; margin: 10px;"
                    ),
                    style="width: 24%; display: inline-block; vertical-align: top;"
                )
                for article in matched_articles
            ],
            style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;"
        ) if matched_articles else P(f"ไม่พบผลลัพธ์ที่เกี่ยวข้องกับ '{query}'")

    @rt('/add_article')
    async def post(req):
        form_data = await req.form()
        title = form_data.get("title", "").strip()
        href = form_data.get("href", "").strip()
        description = form_data.get("description", "").strip()
        content = form_data.get("content", "").strip()
        rating = int(form_data.get("rating", 0))  # Get the star rating
        uploaded_image = form_data.get("image")

        if not uploaded_image or not hasattr(uploaded_image, "filename") or not uploaded_image.filename:
            return P("กรุณาอัปโหลดรูปภาพ", style="color: red;")

        image_filename = uploaded_image.filename
        image_path = os.path.join(__UPLOAD_FOLDER, image_filename)
        try:
            with open(image_path, "wb") as f:
                f.write(await uploaded_image.read())
            image_url = f"/Articleimage/{image_filename}"
            Article.add_article(title, href, image_url, description, content, rating)  # Pass the rating to the new article
            return P("บทความถูกเพิ่มแล้ว!", style="color: green;")
        except Exception as e:
            return P("เกิดข้อผิดพลาดในการบันทึกไฟล์", style="color: red;")

    @rt('/updates')
    def get():
        return Titled(
            "Updates",
            P("อัพเดตล่าสุด: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
