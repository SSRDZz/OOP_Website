from fasthtml.common import *  # type: ignore
from BackEnd import *  # type: ignore
from CustomizeTour import * 
app, rt = fast_app()  # type: ignore

@rt('/')
def get(): #First Time in Website
    return Titled("Sign In",Form(
                P("UserName"),
                Label(Input(id="userName", type="type", placeholder="enter username")),
                P("PassWord"),
                Label(Input(id="password", type="type", placeholder="enter password")),
                A("No Account?",onclick = "location.href='/SignUpPage'"),
                Div(Button("Sign In", type="button", hx_post="/SignInBackEnd")),
                method="post",
                onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                ))

@rt('/SignInAgain') #Come back from sign In
def get():
    return Titled("Sign In",Form(
                P("UserName"),
                Label(Input(id="userName", type="type", placeholder="enter username")),
                P("PassWord"),
                Label(Input(id="password", type="type", placeholder="enter password")),
                A("No Account?",onclick = "location.href='/SignUpPage'"),
                Div(Button("Sign In", type="button", hx_post="/SignInBackEnd")),
                method="post",
                onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                ))

@rt('/SignUpPage')
def get():
    return Titled("Sign Up",Form(
                P("UserName"),
                Label(Input(id="newUserName", type="type", placeholder="Enter username")),
                P("PassWord"),
                Label(Input(id="newPassword", type="type", placeholder="Enter password")),
                Button("Sign Up", type="button", hx_post="/SignUpBackEnd",onclick="location.href='/SignInAgain'"),
                method="post",
                onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                ))

@rt('/SignInBackEnd',methods=["POST"])
def post(userName,password):
    if(website.TryLogIn(userName,password) == True):
        return "Sign in success"
    else:
        return "Log In Fail"
    
@rt('/SignUpBackEnd',methods=["POST"])
def post(newUserName,newPassword):
    website.create_account(newUserName,newPassword)
    return "Sign up success"

serve()