
import psycopg2
from systemEnum import PirorityEnum, TaskStatus
from datetime import datetime

class Database:
    def __init__(self):
        hostname = 'localhost'
        database = 'task_management'
        username = 'postgres'
        pwd = 'root'
        port = '5432'
        self.con = psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port)
        self.cur = self.con.cursor()
    
    def login(self, username, password):
        #applying empty validation
        message = ''
        returnData = dict()
        if username=='' or password=='':
            message = "fill the empty field!!!"
        else:
            self.cur.execute("select * from login(%s,%s)", [username, password])
            
            result = self.cur.fetchone()
            print(result)
            #fetch data 
            if result:
                message = "Login success"
                returnData['employeeId'] = result[0]
                returnData['id'] = result[0]
                returnData['name'] = result[1]
                
            else:
                message = "Wrong username or password!!!"
        returnData['message'] = message
        return returnData

    def getAllTasks(self):
        self.cur.execute("""
            SELECT * FROM view_task_active
        """)
        rows = self.cur.fetchall()
        return rows

    def getAllAuditLogs(self):
        self.cur.execute("""
            SELECT * FROM view_audit_log;
        """)
        rows = self.cur.fetchall()
        return rows
    
    def getOneTask(self, taskId: int):
        cursor = self.cur.execute("""
        SELECT 
            tt.*,
            te.name assign_employee_name,
            te2.name create_employee_name,
            te3.name updated_employee_name
        FROM tbl_task tt
        left join tbl_employee te on te.id = tt.assign_employee_id
        left join tbl_employee te2 on te2.id = tt.created_by
        left join tbl_employee te3 on te3.id = tt.updated_by
        where tt.id = %s
        """%(taskId))
        result = self.cur.fetchone()
        if (result):
            return result
        else:
            print('not found')

    def getAllEmployee(self):
        self.cur.execute("""
            SELECT 
                *
            FROM tbl_employee
        """)
        rows = self.cur.fetchall()
        return rows

    def closeTask(self, taskId: int):
        self.cur.execute("call close_task(%s)", [taskId])
        self.con.commit()
        
    def insertOrUpdate(self,taskId, title, description, priority, startDate, dueDate, assigneeName, currentEmpId, taskStatus):
        now = datetime.now()
        currentDatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        priorityValue = None
        finalStartDate = None
        finalDueDate = None
        if (priority) :
            priorityValue = priority
        if (startDate) :
            finalStartDate = startDate
        if (dueDate):
            finalDueDate = dueDate
        assigneeId = None
        if (assigneeName) :
            self.cur.execute("SELECT * from tbl_employee where name='%s'"%(assigneeName))
            result = self.cur.fetchone()
            #fetch data 
            if result:
                assigneeId = result[0]

        try:
            if (taskId) :
                self.cur.execute("call update_task(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [taskId, title, description, priority, taskStatus, finalStartDate, finalDueDate, assigneeId, currentEmpId, currentDatetime])
            else :
                self.cur.execute("call insert_task(%s,%s,%s,%s,%s,%s,%s,%s,%s)", [title, description, priority, taskStatus, finalStartDate, finalDueDate, assigneeId, currentEmpId, currentDatetime])
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            raise e
            
            
        
