
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
            self.cur.execute("SELECT * from tbl_employee where username='%s' and password='%s'"%(username,password))
            result = self.cur.fetchone()
            #fetch data 
            if result:
                print(result)
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
            SELECT 
                t.*,
                te2.name created_by_employee,
                te.name assign_employee_name
            FROM tbl_task t
            inner join tbl_employee te2 on te2.id = t.created_by
            left join tbl_employee te on te.id = t.assign_employee_id
            where t.status <> 'CLOSED'
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

    def closeTask(self, taskId):
        self.cur.execute("""
            UPDATE tbl_task SET status=%s where id=%s
        """, ('CLOSED', taskId))
        self.con.commit()
        
    def insertOrUpdate(self,taskId, title, description, priority, startDate, dueDate, assigneeName, currentEmpId, taskStatus):
        now = datetime.now()
        currentDatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        priorityValue = None
        if (priority) :
            priorityValue = priority
        assigneeId = None
        if (assigneeName) :
            self.cur.execute("SELECT * from tbl_employee where name='%s'"%(assigneeName))
            result = self.cur.fetchone()
            #fetch data 
            if result:
                assigneeId = result[0]

        if (taskId) :
            self.cur.execute("""
                             UPDATE tbl_task SET title=%s, description=%s, priority=%s, status=%s, start_date=%s, due_date=%s, assign_employee_id=%s,updated_by=%s, updated_date=%s where id=%s
                             """, (title, description, priority, taskStatus, startDate, dueDate, assigneeId, currentEmpId, currentDatetime, taskId))
        else :
            self.cur.execute("INSERT INTO tbl_task(title, description, priority, status, start_date, due_date, assign_employee_id, created_by, created_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (title, description, priority, taskStatus, startDate, dueDate, assigneeId, currentEmpId, currentDatetime))
        self.con.commit()
