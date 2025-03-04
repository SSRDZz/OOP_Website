from fasthtml.common import *
from datetime import datetime
from BackEnd import *
import os

app, rt = fast_app()


# Directory where uploaded images will be stored
UPLOAD_FOLDER = "./Articleimage/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

# Store articles in a list
articles = [
    {"title": "รีวิวการไปเที่ยวญี่ปุ่น", "href": "japan", "image": "/Articleimage/Japan.jpg", "description": "ประสบการณ์การท่องเที่ยวประเทศญี่ปุ่นที่น่าตื่นเต้น!"},
    {"title": "wow", "href": "welcome", "image": "/Articleimage/japan1.jpg", "description": "dis"}
]

# Function to add a new article
def add_article(title, href, image_path, description):
    articles.append({"title": title, "href": href, "image": image_path, "description": description})

@rt('/Articleimage/<filename>')
def get_uploaded_image(req, filename):
    """ Serve uploaded images """
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        print(f"❌ File Not Found: {file_path}")
        return P("File not found", style="color: red;")

    return FileResponse(file_path)  # ✅ Serve the actual image file

@rt('/')
def get():
    """ Main page with search and upload form """
    return Titled("Article",
        Form(
            Input(
                name="query",
                placeholder="พิมพ์เพื่อค้นหา...",
                hx_get="/search",
                hx_trigger="keyup delay:500ms",
                hx_target="#search-results"
            ),
            Div(id="search-results")  # Display search results here
        ),
        (Form(
            H3("เพิ่มบทความใหม่"),
            Input(name="title", placeholder="Title"),
            Input(name="href", placeholder="URL"),
            Input(name="image", type="file"),  # File upload input
            Input(name="description", placeholder="Description"),
            Button("Add Article", hx_post="/add_article", hx_encoding="multipart/form-data")
        ) if isinstance(website.currentUser, Staff) else None),
        Div(
            id="update-section",
            hx_get="/updates",
            hx_trigger="every 3s"
        ),
        Div(
            *[
                Div(
                    Card(
                        Img(src=article["image"]),
                        H3(A(article["title"], href=article["href"], style="color: #1976d2;")),
                        P(article["description"]),
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

@rt('/search')
def get(req):
    """ Search articles by title or description """
    query = req.query_params.get("query", "").strip().lower()

    if not query:
        return P("กรุณากรอกข้อความค้นหา")  # No search term entered

    matched_articles = [
        article for article in articles
        if query in article["title"].lower() or query in article["description"].lower()
    ]

    return Div(
        *[
            Div(
                Card(
                    Img(src=article["image"]),
                    H3(A(article["title"], href=article["href"], style="color: #1976d2;")),
                    P(article["description"]),
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
    """ Handles article upload and saves the image file """
    form_data = await req.form()
    print("✅ Received form data:", form_data)

    title = form_data.get("title", "").strip()
    href = form_data.get("href", "").strip()
    description = form_data.get("description", "").strip()
    uploaded_image = form_data.get("image")

    # Ensure file is uploaded
    if not uploaded_image:
        print("❌ No file uploaded!")
        return P("กรุณาอัปโหลดรูปภาพ", style="color: red;")

    # Check if file has a valid filename
    if not hasattr(uploaded_image, "filename") or not uploaded_image.filename:
        print("❌ Uploaded image has no filename!")
        return P("ไฟล์รูปภาพไม่ถูกต้อง", style="color: red;")

    # Save the file
    image_filename = uploaded_image.filename
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)

    try:
        with open(image_path, "wb") as f:
            f.write(await uploaded_image.read())  # Read and write file content

        print(f"✅ Image saved: {image_path}")

        # Create accessible URL for the uploaded image
        image_url = f"/Articleimage/{image_filename}"

        # Add new article to the list
        add_article(title, href, image_url, description)

        return P("บทความถูกเพิ่มแล้ว!", style="color: green;")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return P("เกิดข้อผิดพลาดในการบันทึกไฟล์", style="color: red;")

@rt('/updates')
def get():
    """ Update section """
    return P(f"อัปเดตล่าสุด: {datetime.now().strftime('%H:%M:%S')}")

serve()
