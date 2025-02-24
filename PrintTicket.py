from fasthtml.common import *
from dataclasses import dataclass

app, rt = fast_app()





@rt("/")
def get():
    return Titled(
        Div(
            Button(
                "Print Ticket",
                onclick="",  
                Style="""
                    display: block;
                    position: absolute;
                    left: 15%;
                    top: 10px;
                    width: 70%;
                    border: solid;
                    background-color: #ffffff;
                    color: orange;
                    font-weight : bold;
                    padding: 10px;
                    font-size: 25px;
                    cursor: pointer;
                    text-align: center;       
                """
            ),
            
        ),
        Grid(
            Card(
                H3("Transaction ID : "),
                Div(style="border: 1px solid #ccc; padding: 150px;"),
                Div(style="border: 1px solid #ccc; padding: 50px; margin-top: 20px;"),
                
                Style = "text-align:left; background-color: #ffffff; margin:80px; width:100%"
            ),
        
            Card(
                H3("ชำระเงินโดย : "),
                Div(style="border: 1px solid #ccc; padding: 50px; margin-top: 20px;"),  
                Style = "text-align:left; background-color: #ffffff; margin:80px;"
            ),
        )
        
        
        
    )       

        

serve()

