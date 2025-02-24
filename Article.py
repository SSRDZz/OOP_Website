from fasthtml.common import *
from datetime import datetime
from BackEnd import *
app, rt = fast_app()

articles = [
    Article(
        "รีวิวการไปเที่ยวญี่ปุ่น",
        "https://example.com",
        "https://media.vogue.in/wp-content/uploads/2018/04/Your-ultimate-guide-to-Tokyo-Japan1.jpg",
        "ประสบการณ์การท่องเที่ยวประเทศญี่ปุ่นที่น่าตื่นเต้น!"
    ),
    Article(
        "รีวิวการไปเที่ยวเกาหลี",
        "https://example.com/korea",
        "https://example.com/korea_image.jpg",
        "ท่องเที่ยวเกาหลีใต้ และสถานที่น่าสนใจ"
    ),
    Article(
        "รีวิวการไปเที่ยวฝรั่งเศส",
        "https://example.com/france",
        "https://example.com/france_image.jpg",
        "ดื่มด่ำกับความโรแมนติกในกรุงปารีส ฝรั่งเศส"
    ),
]

# Function to add new articles
def add_article(title, href, image, description):
    new_article = Article(title, href, image, description)
    articles.append(new_article)

@rt('/')
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
            Div(id="search-results")  # ส่วนแสดงผลลัพธ์การค้นหา
        ),
        Form(
            H3("Add New Article"),
            Input(name="title", placeholder="Title"),
            Input(name="href", placeholder="URL"),
            Input(name="image", placeholder="Image URL"),
            Input(name="description", placeholder="Description"),
            Button("Add Article", hx_post="/add_article", hx_trigger="click")
        ),
        Div(
            id="update-section",
            hx_get="/updates",
            hx_trigger="every 3s"
        ),
        
        # Show all cards in a grid with 4 per row
        Div(
            *[
                Div(
                    Card(
                        Img(src=article.image),
                        H3(A(article.title, href=article.href, style="color: #1976d2;")),
                        P(article.description),
                        style="""
                            border: 2px solid #2196f3;
                            border-radius: 10px;
                            padding: 20px;
                            margin: 10px;
                        """
                    ),
                    style="width: 24%; display: inline-block; vertical-align: top;"
                )
                for article in articles
            ],
            style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;"
        )
    )

@rt('/search')
def get(req):
    query = req.query_params.get("query", "").strip()
    
    if query:
        # Search for articles
        matched_articles = [
            article for article in articles if query in article.title or query in article.description
        ]
        
        if matched_articles:
            # Return matched articles
            return Div(
                *[
                    Div(
                        Card(
                            Img(src=article.image),
                            H3(A(article.title, href=article.href, style="color: #1976d2;")),
                            P(article.description),
                            style="""
                                border: 2px solid #2196f3;
                                border-radius: 10px;
                                padding: 20px;
                                margin: 10px;
                            """
                        ),
                        style="width: 24%; display: inline-block; vertical-align: top;"
                    )
                    for article in matched_articles
                ],
                style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;"
            )
        else:
            return P(f"ไม่พบผลลัพธ์ที่เกี่ยวข้องกับ '{query}'")
    else:
        # If no query is provided
        return Div(
            *[
                Div(
                    Card(
                        Img(src=article.image),
                        H3(A(article.title, href=article.href, style="color: #1976d2;")),
                        P(article.description),
                        style="""
                            border: 2px solid #2196f3;
                            border-radius: 10px;
                            padding: 20px;
                            margin: 10px;
                        """
                    ),
                    style="width: 24%; display: inline-block; vertical-align: top;"
                )
                for article in articles
            ],
            style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;"
        )

@rt('/add_article')
def post(req):
    title = req.form.get("title", "").strip()
    href = req.form.get("href", "").strip()
    image = req.form.get("image", "").strip()
    description = req.form.get("description", "").strip()

    if title and href and image and description:
        add_article(title, href, image, description)
        return P("บทความถูกเพิ่มแล้ว!", style="color: green;")
    else:
        return P("กรุณากรอกข้อมูลให้ครบถ้วน", style="color: red;")

@rt('/updates')
def get():
    return P(f"อัปเดตล่าสุด: {datetime.now().strftime('%H:%M:%S')}")

serve()
