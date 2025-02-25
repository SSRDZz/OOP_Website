from fasthtml.common import *  # type: ignore
from datetime import datetime
from BackEnd import *  # type: ignore

app, rt = fast_app()  # type: ignore

@rt('/')
def get():
    return Titled("MainPage")

serve()