from fasthtml.common import *
from datetime import datetime
from Article import *
from BackEnd import *

@rt('/japan')
def get():
    return Head(Title("Welcome"),
            Body(
                Div(H1("รีวิวการไปการไป",Style = "text-align:center")),
                    Div(Img(src="/Articleimage/Japan.jpg"),style="text-align:center"),
                    H4('สนุกมากๆครับomg'),
                    Button("Omg",style="width:150px;,margin-top:10px;",onclick="location.href='/'")
                    
                
                )
            )
        

serve()