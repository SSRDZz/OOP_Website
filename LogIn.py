#LogIn.py
from fasthtml.common import *  # type: ignore
from BackEnd import *  # type: ignore

def register_routes(rt):
    @rt('/')
    def get():  # First time in Website
        return Titled("Sign In", Form(
                    P("UserName"),
                    Label(Input(id="userName", type="text", placeholder="enter username")),  # type="text" for username
                    P("PassWord"),
                    Label(Input(id="password", type="password", placeholder="enter password")),  # type="password" for password
                    A("No Account?", onclick="location.href='/SignUpPage'"),
                    Div(Button("Sign In", type="button", hx_post="/SignInBackEnd", hx_target="body")),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                    ))

    @rt('/SignInAgain')  # Come back from sign In
    def get():
        return Titled("Sign In", Form(
                    P("UserName"),
                    Label(Input(id="userName", type="text", placeholder="enter username")),  # type="text" for username
                    P("PassWord"),
                    Label(Input(id="password", type="password", placeholder="enter password")),  # type="password" for password
                    A("No Account?", onclick="location.href='/SignUpPage'"),
                    Div(Button("Sign In Failed", type="button", hx_post="/SignInBackEnd", hx_target= "body")),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                    ))

    @rt('/SignUpPage')
    def get():
        return Titled("Sign Up", Form(
                    P("UserName"),
                    Label(Input(id="newUserName", type="text", placeholder="Enter username")),  # type="text" for username
                    P("PassWord"),
                    Label(Input(id="newPassword", type="password", placeholder="Enter password")),  # type="password" for password
                    Button("Sign Up as User", type="button", hx_post="/SignUpUser",onclick="location.href='/'"),
                    Button("Sign Up Staff", type="button", hx_post="/SignUpStaff",onclick="location.href='/'"),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                    ))

    @rt('/SignInBackEnd', methods=["POST"])
    def post(userName : str, password : str):
        if website.TryLogIn(userName, password):
            return Redirect("/MainPage")
        else:
            return Redirect("/SignInAgain")

    @rt('/SignUpUser', methods=["POST"])
    def post(newUserName : str, newPassword : str):
        website.create_account(newUserName, newPassword)
        return "Sign up success"
    
    @rt('/SignUpStaff', methods=["POST"])
    def post(newUserName : str, newPassword : str):
        website.create_staff_account(newUserName, newPassword)
        return "Sign up success"


