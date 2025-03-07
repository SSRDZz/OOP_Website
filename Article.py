from fasthtml.common import *
from datetime import datetime
from BackEnd import *
import os

UPLOAD_FOLDER = "./Articleimage/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

articles = [
    Article("รีวิวการไปเที่ยวญี่ปุ่น", "japan", "/Articleimage/Japan.jpg", "ประสบการณ์การท่องเที่ยวประเทศญี่ปุ่นที่น่าตื่นเต้น!", "รายละเอียดการเดินทางไปญี่ปุ่น..."),
    Article("wow", "welcome", "/Articleimage/japan1.jpg", "dis", "เนื้อหาเพิ่มเติมเกี่ยวกับบทความ wow")
]

# Function to add a new article
def add_article(title, href, image_path, description, content):
    sanitized_href = href.lower().replace(" ", "-")  # Ensure URL safety
    new_article = Article(title, sanitized_href, image_path, description, content)
    articles.append(new_article)

def register_routes(rt):
    @rt('/Articleimage/<filename>')
    def get_uploaded_image(req, filename):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
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
                Button("Add Article", hx_post="/add_article", hx_encoding="multipart/form-data")
            ) if isinstance(website.currentUser, Staff) else None),
            Div(
                *[
                    Div(
                        Card(
                            Img(src=article.get_image()),
                            H3(A(article.get_title(), href=f"/article/{article.get_href()}", style="color: #1976d2;")),
                            P(article.get_description()),
                            style="border: 2px solid #2196f3; border-radius: 10px; padding: 20px; margin: 10px;"
                        ),
                        style="width: 24%; display: inline-block; vertical-align: top;"
                    )
                    for article in articles
                ],
                id="article-list",
                style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;"
            )
        )

    @rt('/Article/<href>')
    def get(req, href):
        """ Display full article details """
        href = href.lower()  # Ensure lowercase comparison
        article = next((a for a in articles if a.get_href() == href), None)

        if not article:
            return P("บทความไม่พบ", style="color: red;")

        return Titled(article.get_title(),
            Img(src=article.get_image()),
            P(article.get_description()),
            P(article.get_content())
        )

    @rt('/search')
    def get(req):
        query = req.query_params.get("query", "").strip().lower()
        if not query:
            return P("กรุณากรอกข้อความค้นหา")
        matched_articles = [
            article for article in articles
            if query in article.get_title().lower() or query in article.get_description().lower()
        ]
        return Div(
            *[
                Div(
                    Card(
                        Img(src=article.get_image()),
                        H3(A(article.get_title(), href=f"/article/{article.get_href()}", style="color: #1976d2;")),
                        P(article.get_description()),
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
        uploaded_image = form_data.get("image")

        if not uploaded_image or not hasattr(uploaded_image, "filename") or not uploaded_image.filename:
            return P("กรุณาอัปโหลดรูปภาพ", style="color: red;")

        image_filename = uploaded_image.filename
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        try:
            with open(image_path, "wb") as f:
                f.write(await uploaded_image.read())
            image_url = f"/Articleimage/{image_filename}"
            add_article(title, href, image_url, description, content)
            return P("บทความถูกเพิ่มแล้ว!", style="color: green;")
        except Exception as e:
            return P("เกิดข้อผิดพลาดในการบันทึกไฟล์", style="color: red;")

    @rt('/updates')
    def get():
        return P(f"อัปเดตล่าสุด: {datetime.now().strftime('%H:%M:%S')}")
