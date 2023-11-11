from tkinter import *
from tkinter import ttk
from db.db import Database
from utils import *
from tkcalendar import Calendar, DateEntry
from systemEnum import PirorityEnum, TaskStatus

ROOT = Tk()

TABLE = ttk.Treeview()
ROOT.title("Task Management System")
ROOT.geometry("1366x710")
ROOT.config(bg="Whitesmoke")
# ROOT.attributes('-fullscreen', True)
ROOT.attributes('-zoomed', True)

# variable
currentEmployeeLoginName = StringVar()
currentEmployeeLoginId = IntVar()
frameBackgroundColor = "#ffffff"
valueTitle = StringVar()
valueDescription = StringVar()
valuePriority = StringVar()
valueStartDate = StringVar()
valueDueDate = StringVar()
valueAssignee = StringVar()
valueStatus = StringVar()
valueTaskId = IntVar()

# header
headerFrame = Frame(ROOT, height=50, bg='grey')
headerFrame.pack(side="top", fill="x")

# logout icon
logoutIcon= PhotoImage(file='./icon/logout_32px.png')
logoutLabel = Label(headerFrame, image = logoutIcon, bg='grey')
logoutLabel.pack(side=RIGHT)

# user icon
userIcon= PhotoImage(file='./icon/user_32px.png')
labelIcon = Label(headerFrame, image = userIcon, bg='grey')
labelIcon.pack(side=LEFT)

labelUsername = Label(headerFrame, textvariable=currentEmployeeLoginName, bg='grey',fg='white', justify=CENTER)
labelUsername.pack(side=LEFT)

# Main Form
mainFrame = Frame(ROOT, height=900, bg=frameBackgroundColor)
createFrame = Frame(ROOT, height=900, bg=frameBackgroundColor)

# Footer
footFrame = Frame(ROOT, height=50, bg='grey')
footFrame.pack(side="bottom", fill=X)
    
def homePage(employeeInformation: tuple, db: Database):
    currentEmployeeLoginName.set(employeeInformation['name'])
    currentEmployeeLoginId.set(employeeInformation['id'])
    getAllTaskToTable(db)
    ROOT.mainloop()

def formAuditLog(db: Database):
    mainFrame.pack_forget()
    
def formNewTask(db: Database, taskId: int):
    mainFrame.pack_forget()
    valueTaskId.set(0 if taskId is None else taskId)
    createFrame.pack(fill=BOTH)
    col3Width = 200
    
    lblTaskName = Label(createFrame, text="Task Name", bg=frameBackgroundColor)
    lblTaskName.grid(row=0, column=0,columnspan=3, padx=(50,20), pady=20, sticky="w")
    txtTaskName = Entry(createFrame, width=col3Width, textvariable=valueTitle)
    txtTaskName.grid(row=1,column=0, columnspan=3, padx=(50,20), sticky="w")

    lblTaskDescription = Label(createFrame, text="Task Description", bg=frameBackgroundColor)
    lblTaskDescription.grid ( row=2, column=0,columnspan=3, padx=(50,20),pady=5, sticky="w")
    txtTaskDescription = Text(createFrame, height=30, width=col3Width)
    txtTaskDescription.grid(row=3,column=0, columnspan=3, rowspan=30, padx=(50,20), sticky="w")
    
    btnList = Button(createFrame, text="List", width=10, fg="white", bg="gray", bd=0)
    btnList.grid(row=34, column=0, padx=0, pady=10, sticky=E)
    btnList.bind('<Button-1>', lambda e: onButtonBackToList(db))
    
    btnClose = Button(createFrame, text="Close", width=10, fg="white", bg="red", bd=0)
    btnClose.grid(row=34, column=1, padx=(10,0),pady=10, sticky=E)
    btnClose.bind('<Button-1>', lambda e: onButtonClose(db))
    
    btnSave = Button(createFrame, text="Create", width=10, fg="white", bg="green", bd=0)
    btnSave.grid(row=34, column=2, padx=(10,20),pady=10, sticky=E)
    btnSave.bind('<Button-1>', lambda e: onButtonSave(db, txtTaskDescription))
    if (taskId):
        btnSave.configure(text="Update")
    else:
        btnSave.configure(text="Create")
        
    # column right side
    
    lblStatus = Label(createFrame, text="Status", bg=frameBackgroundColor)
    lblStatus.grid(row=0, column=3, sticky="w", padx=(0,50), pady=5)
    comboPriority = ttk.Combobox(createFrame, width=30, state="readonly", textvariable=valueStatus)
    comboPriority.grid(row=1, column=3, sticky="w", padx=(0,50))
    comboPriority['values'] = tuple(convert_upper_underscore_to_capitalize(enum.value) for enum in TaskStatus)
    createFrame.grid_columnconfigure(0, weight=1)
    
    lblAssignees = Label(createFrame, text="Assignees", bg=frameBackgroundColor)
    lblAssignees.grid(row=2, column=3, sticky="w", padx=(0,50), pady=5)
    empFromDb = db.getAllEmployee()
    comboAssignees = ttk.Combobox(createFrame, width=30, state="readonly", values=[item[1] for item in empFromDb], textvariable=valueAssignee)
    comboAssignees.grid(row=3, column=3, sticky="w", padx=(0,50))
    
    lblPriority = Label(createFrame, text="Priority", bg=frameBackgroundColor)
    lblPriority.grid(row=4, column=3, sticky="w", padx=(0,50), pady=5)
    comboPriority = ttk.Combobox(createFrame, width=30, state="readonly", textvariable=valuePriority)
    comboPriority.grid(row=5, column=3, sticky="w", padx=(0,50))
    comboPriority['values'] = tuple(convert_upper_underscore_to_capitalize(enum.value) for enum in PirorityEnum)
    createFrame.grid_columnconfigure(0, weight=1)
    
    lblStartDate = Label(createFrame, text="Start Date", bg=frameBackgroundColor)
    lblStartDate.grid(row=6, column=3, sticky="w", padx=(0,50), pady=5)
    startDate = DateEntry(createFrame, width= 30, background= "magenta3", foreground= "white",bd=2, textvariable=valueStartDate)
    startDate.grid(row=7, column=3, sticky="w", padx=(0,50))
    
    lblDueDate = Label(createFrame, text="Due Date", bg=frameBackgroundColor)
    lblDueDate.grid(row=8, column=3, sticky="w", padx=(0,50), pady=5)
    dueDate = DateEntry(createFrame, width= 30, background= "magenta3", foreground= "white",bd=2, textvariable=valueDueDate)
    dueDate.grid(row=9, column=3, sticky="w", padx=(0,50))
    
    # handle update
    if (taskId) :
        data = db.getOneTask(taskId)
        title = data[1]
        description = data[2]
        priority = data[3]
        status = data[4]
        startDate = data[5]
        dueDate = data[6]
        assignee = data[12]
        
        valueTitle.set("" if title is None else title)
        txtTaskDescription.insert(END, "" if description is None else description)
        valuePriority.set(convert_upper_underscore_to_capitalize(priority))
        valueStatus.set(convert_upper_underscore_to_capitalize(status))
        valueStartDate.set(startDate)
        valueDueDate.set(dueDate)
        valueAssignee.set(assignee)
    else:
        valueTitle.set("")
        txtTaskDescription.insert(END, "")
        valuePriority.set("")
        valueStatus.set("")
        valueStartDate.set("")
        valueDueDate.set("")
        valueAssignee.set("")
        
def onButtonClose(db: Database):
    taskId = valueTaskId.get()
    print(taskId)
    db.closeTask(taskId)
    onButtonBackToList(db)
    
def onButtonSave(db: Database, txtTaskDescription: Text):
    title = valueTitle.get()
    description = txtTaskDescription.get(1.0, END)
    priority = convert_string_to_upper_underscore(valuePriority.get())
    status = convert_string_to_upper_underscore(valueStatus.get())
    startDate = valueStartDate.get()
    dueDate = valueDueDate.get()
    assigneeName = valueAssignee.get()
    taskId = valueTaskId.get()

    db.insertOrUpdate(taskId, title, description, priority, startDate, dueDate, assigneeName, currentEmployeeLoginId.get(), status)
    onButtonBackToList(db)
    
def onButtonBackToList(db: Database) :
    createFrame.forget()
    getAllTaskToTable(db)
    
def onButtonNewTask(db: Database):
    formNewTask(db, None)

def onButtonLog(db: Database):
    getAllAuditLog(db)
    
def onSelectTableRow(db: Database, table: ttk.Treeview):
    for i in table.selection():
        item = table.item(i)
        record = item['values']
        taskId = record[0]
        print(taskId)
        formNewTask(db, taskId)

def getAllAuditLog(db: Database):
    # clear all widget
    for widget in mainFrame.winfo_children():
       widget.destroy()
       
    headerColumns = ('No', 'Description', 'Created Date')
    table = ttk.Treeview(mainFrame, columns=headerColumns, show='headings')

    for header in headerColumns:
        table.heading(header, text=header)
        # table.column("#0", minwidth=0, width=5, stretch=YES)
    
    dataFromDb = db.getAllAuditLogs()

    index = 0
    for data in dataFromDb:
        index += 1
        no = index
        description = data[1]
        createdDate = data[2]
        
        displayTableRow = (index, description, createdDate)
        table.insert('', END, values=displayTableRow)
    
    btnList = Button(mainFrame, text="Home", width=10, fg="white", bg="gray", bd=0)
    btnList.pack(ipady=5, pady=20, padx=50, anchor='nw')
    btnList.bind('<Button-1>', lambda e: onButtonBackToList(db))
    
    table.pack(fill="x", padx=50)
    mainFrame.pack(fill=BOTH)
    
def getAllTaskToTable(db: Database):
    # clear all widget
    for widget in mainFrame.winfo_children():
       widget.destroy()
       
    headerColumns = ('Id', 'No', 'Task Name', 'Priority', 'Start Date', 'Due Date', 'Assign', 'Created By', 'Created At', 'Status')
    table = ttk.Treeview(mainFrame, columns=headerColumns, show='headings')
    for header in headerColumns:
        table.heading(header, text=header)
    
    # hidden column id
    table.column("Id", stretch=NO, minwidth=0, width=0)
    dataFromDb = db.getAllTasks()

    index = 0
    for data in dataFromDb:
        index += 1
        no = index
        taskId = data[0]
        taskName = data[1]
        priority = convert_upper_underscore_to_capitalize(data[3])
        startDate = data[5]
        dueDate = data[6]
        assingeName = data[13]
        createdBy = data[12]
        createdAt = data[9]
        status = convert_upper_underscore_to_capitalize(data[4])
        
        displayTableRow = (taskId, index, taskName, priority, startDate, dueDate, assingeName, createdBy, createdAt, status)
        table.insert('', END, values=displayTableRow)

    table.bind('<<TreeviewSelect>>', lambda e: onSelectTableRow(db, table))
    
    btnLog = Button(mainFrame, text="Audit Log", width=15, fg="white", bg="gray", bd=0)
    btnLog.bind('<Button-1>', lambda e: onButtonLog(db))
    btnLog.pack(ipady=5, pady=20, padx=50, anchor='nw')
    
    btnNewTask = Button(mainFrame, text="New Task", width=15, fg="white", bg="green", bd=0)
    btnNewTask.bind('<Button-1>', lambda e: onButtonNewTask(db))
    btnNewTask.pack(ipady=5, pady=20, padx=50, anchor='ne')
    
    table.pack(fill="x", padx=50)
    mainFrame.pack(fill=BOTH)

# db = Database()
# employeeInformation = dict()
# employeeInformation["id"] = 1
# employeeInformation["name"] = "Kong Bunthoeurn"
# homePage(employeeInformation, db)