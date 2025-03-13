#LogIn.py
from fasthtml.common import *  # type: ignore
from BackEnd import *  # type: ignore

def register_routes(rt):
    @rt('/')
    def get():  # First time in Website
        return Titled("Sign In", Form(
                    P("Username",style="text-align: left;"),
                    Label(Input(id="userName", type="text", placeholder="Enter username",style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),  # type="text" for username
                    P("Password",style="text-align: left;"),
                    Label(Input(id="password", type="password", placeholder="Enter password",style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),  # type="password" for password
                    A("No Account?", onclick="location.href='/SignUpPage'"),
                    Div(Button("Sign In", type="button", hx_post="/SignInBackEnd", hx_target="body",style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;")),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                    ),style="background-color: #F5F7F8; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); max-width: 500px; margin: 20px auto; text-align: center;")

    @rt('/SignInAgain')  # Come back from sign In
    def get():
        return Titled("Sign In", Form(
                    P("Username",style="text-align: left;"),
                    Label(Input(id="userName", type="text", placeholder="Enter username",style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),  # type="text" for username
                    Br(),
                    P("Password",style="text-align: left;"),
                    Label(Input(id="password", type="password", placeholder="Enter password",style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),  # type="password" for password
                    A("No Account?", onclick="location.href='/SignUpPage'"),
                    Div(Button("Sign In", type="button", hx_post="/SignInBackEnd", hx_target="body",style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;")),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                    ),style="background-color: #F5F7F8; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); max-width: 500px; margin: 20px auto; text-align: center;")

    @rt('/SignUpPage')
    def get():
        return Titled("Sign Up", Form(
                    P("Username",style="text-align: left;"),
                    Label(Input(id="newUserName", type="text", placeholder="Enter username",style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),  # type="text" for username
                    Br(),
                    P("Password",style="text-align: left;"),
                    Label(Input(id="newPassword", type="password", placeholder="Enter password",style="width: 100%; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")),  # type="password" for password
                    Button("Sign Up as User", type="button", hx_post="/SignUpUser",style="background-color: #FFD700; color: black; padding: 10px 20px; border: none; border-radius: 5px;"),
                    Button("Sign Up as Staff", type="button", hx_post="/SignUpStaff",style="background-color: #FFD700; color: black; padding: 10px 20px;margin-left: 10px; border: none; border-radius: 5px;"),
                    method="post",
                    onkeydown="if(event.key==='Enter'){event.preventDefault();}"
                    ),style="background-color: #F5F7F8; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); max-width: 500px; margin: 20px auto; text-align: center;")

    @rt('/SignInBackEnd', methods=["POST"])
    def post(userName : str, password : str):
        if website.try_log_in(userName, password):
            return Redirect("/MainPage")
        else:
            return Redirect("/SignInAgain")

    @rt('/SignUpUser', methods=["POST"])
    def post(newUserName : str, newPassword : str):
        if(newUserName == "" or newPassword == ""):
            return Redirect("/SignUpPage")
        else:
            website.create_account(newUserName, newPassword)
            return Redirect("/")
    
    @rt('/SignUpStaff', methods=["POST"])
    def post(newUserName : str, newPassword : str):
        if(newUserName == "" or newPassword == ""):
            return Redirect("/SignUpPage")
        else:
            website.create_staff_account(newUserName, newPassword)
            return Redirect("/")


