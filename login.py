from tkinter import *
from db.db import Database

DRIVER_NAME = 'ODBC Driver 11 for SQL Server'
SERVER_NAME = 'KEANTHAI41A7'
DATABASE_NAME = 'TASK_MANAGEMENT'
# uid=<username>;
# pwd=<password>;

# databaseLink = "DRIVER={Devart ODBC Driver for SQL Server};Server=localhost;Database=master;Port=myport;User ID=myuserid;Password=mypassword"
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
db = Database(connection_string)
#db = Database("./db/TASK_MANAGEMENT.db")

def handleLogin():
    user = username.get()
    pwd = password.get()
    responseMessage = db.login(user, pwd)
    print(responseMessage)
    loginMessage = responseMessage['message']
    
    loginEmployeeId = responseMessage['employeeId'] if 'employeeId' in responseMessage else ''
    message.set(loginMessage)
    
    # on success close login form
    if loginEmployeeId:
        login_screen.destroy()
        import index
        index.homePage(responseMessage, db)
    
def Loginform():
    global login_screen
    login_screen = Tk()
    #Setting title of screen
    login_screen.title("Login | Task Management System ")
    #setting height and width of screen
    login_screen.geometry("350x250")
    login_screen.eval('tk::PlaceWindow . center')
    login_screen["bg"]="#ffffff"
    #declaring variable
    global message
    global username
    global password
    username = StringVar()
    password = StringVar()
    message=StringVar()
    #Creating layout of login form
    Label(login_screen,width="300", text="Login From", bg="grey",fg="black",font=("Arial",12,"bold")).pack()
    #Username Label
    Label(login_screen, text="Username * ",bg="#ffffff",fg="black",font=("Arial",12,"bold")).place(x=20,y=40)
    #Username textbox
    Entry(login_screen, textvariable=username,bg="#ffffff",fg="black",font=("Arial",12,"bold")).place(x=120,y=42)
    #Password Label
    Label(login_screen, text="Password * ",bg="#ffffff",fg="black",font=("Arial",12,"bold")).place(x=20,y=80)
    #Password textbox
    Entry(login_screen, textvariable=password ,show="*",bg="#ffffff",fg="black",font=("Arial",12,"bold")).place(x=120,y=82)
    #Label for displaying login status[success/failed]
    Label(login_screen, text="",textvariable=message,bg="#ffffff",fg="black",font=("Arial",12,"bold")).place(x=95,y=120)
    #Login button
    Button(login_screen, text="Login", width=10, height=1, command=handleLogin, bg="grey",fg="black",font=("Arial",12,"bold")).place(x=125,y=170)
    login_screen.mainloop()

Loginform()
