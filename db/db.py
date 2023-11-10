import sqlite3
from systemEnum import PirorityEnum, TaskStatus
from datetime import datetime
import psycopg2

class Database:
    def __init__(self, db):
        hostname = 'localhost'
        database = 'TASK_MANAGEMENT'
        username = 'postgres'
        pwd = '12345'
        port = '5432'
        self.con = psycopg2.connect(host = hostname, dbname = database, user = username, pwd =pwd, port = port)
        self.cur = self.con.cursor()
        sql_employee = """
            CREATE TABLE IF NOT EXISTS tbl_employee(
                id Integer Primary Key,
                name text not null,
                username text not null unique,
                password text not null
            );
        """
        sql_task = """
            CREATE TABLE IF NOT EXISTS tbl_task(
                id Integer Primary Key,
                title text not null,
                description text,
                priority,
                status not null,
                start_date date,
                due_date date,
                assign_employee_id Integer,
                created_by Integer not null,
                created_date datetime not null,
                updated_by Integer null,
                updated_date datetime null,
                FOREIGN KEY(assign_employee_id) REFERENCES tbl_employee(id),
                FOREIGN KEY(created_by) REFERENCES tbl_employee(id),
                FOREIGN KEY(updated_by) REFERENCES tbl_employee(id)
            );
        """
        self.cur.execute(sql_employee)
        self.cur.execute(sql_task)
        self.con.commit()
    
    def login(self, username, password):
        #applying empty validation
        message = ''
        returnData = dict()
        if username=='' or password=='':
            message = "fill the empty field!!!"
        else:
            cursor = self.cur.execute('SELECT * from tbl_employee where username="%s" and password="%s"'%(username,password))
            result = cursor.fetchone()
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
        result = cursor.fetchone()
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
            UPDATE tbl_task SET status=? where id=?
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
            cursor = self.cur.execute('SELECT * from tbl_employee where name="%s"'%(assigneeName))
            result = cursor.fetchone()
            #fetch data 
            if result:
                assigneeId = result[0]

        if (taskId) :
            self.cur.execute("""
                             UPDATE tbl_task SET title=?, description=?, priority=?, status=?, start_date=?, due_date=?, assign_employee_id=?,updated_by=?, updated_date=? where id=?
                             """, (title, description, priority, taskStatus, startDate, dueDate, assigneeId, currentEmpId, currentDatetime, taskId))
        else :
            self.cur.execute("INSERT INTO tbl_task(title, description, priority, status, start_date, due_date, assign_employee_id, created_by, created_date) VALUES (?,?,?,?,?,?,?,?,?)",
                         (title, description, priority, taskStatus, startDate, dueDate, assigneeId, currentEmpId, currentDatetime))
        self.con.commit()
