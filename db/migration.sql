CREATE OR REPLACE FUNCTION insert_task_log()
  RETURNS trigger AS

$$
begin
    INSERT INTO tbl_log (created_by, description) VALUES(new.created_by, concat('user create task id = ', new.id, ', task name = ', new.title));
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER task_insert_trigger
  AFTER INSERT
  ON "tbl_task"
  FOR EACH ROW
  EXECUTE PROCEDURE insert_task_log();
  
CREATE OR REPLACE FUNCTION update_task_log()
  RETURNS trigger AS

$$
begin
    INSERT INTO tbl_log (created_by, description) 
   VALUES(new.created_by, concat('user has been update task id = ', new.id, ', task name = ', old.title, ' -> ', new.title, ', status = ', old.status, ' -> ', new.status));
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER task_update_trigger
  AFTER UPDATE
  ON "tbl_task"
  FOR EACH ROW
  EXECUTE PROCEDURE update_task_log();


CREATE OR REPLACE PROCEDURE close_task(IN taskId int)
LANGUAGE plpgsql
AS $$
BEGIN
  update tbl_task set status = 'CLOSED' where id = taskId;
END;
$$;

-- View task active

CREATE OR REPLACE VIEW view_task_active as
	SELECT 
        t.*,
        te2.name created_by_employee,
        te.name assign_employee_name
    FROM tbl_task t
    inner join tbl_employee te2 on te2.id = t.created_by
    left join tbl_employee te on te.id = t.assign_employee_id
    where t.status <> 'CLOSED';


CREATE OR REPLACE VIEW view_audit_log as
	SELECT 
        tl.*,
        te."name" create_by_name
    FROM tbl_log tl
    left join tbl_employee te on te.id = tl.created_by;


CREATE OR REPLACE FUNCTION login(inputUsername varchar, inputPassword varchar) 
    RETURNS TABLE (
        employee_id int,
        "employee_name" varchar(255),
        "employee_username" varchar(255)
) 
AS $$
BEGIN
    RETURN QUERY SELECT
        "id" as employee_id,
        cast("name" as varchar) as employee_name,
        cast("username" as varchar) as employee_username
    FROM
        tbl_employee
    WHERE
        "username" = inputUsername and "password" = inputPassword;
END; $$ 

LANGUAGE 'plpgsql';

CREATE OR REPLACE PROCEDURE insert_task(
  IN title TEXT,
  in description text,
  in priority text,
  in status text,
  in start_date text,
  in due_date text,
  in assign_employee_id int,
  in created_by int,
  in created_date text
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO tbl_task (title, description, priority, status, start_date, due_date, assign_employee_id, created_by, created_date)
  VALUES (title, description, priority, status, cast(start_date as date), cast(due_date as date), assign_employee_id, created_by, cast(created_date as timestamp));
END;
$$;


CREATE OR REPLACE PROCEDURE update_task(
  in taskId int,
  IN updateTitle TEXT,
  in updateDescription text,
  in updatePriority text,
  in updateStatus text,
  in updateStartDate text,
  in updateDueDate text,
  in updateAssignEmployeeId int,
  in inputUpdatedBy int,
  in inputUpdatedDate text
)
LANGUAGE plpgsql
AS $$
begin
  UPDATE tbl_task SET 
 	title=updateTitle,
 	description=updateDescription,
 	priority=updatePriority,
 	status=updateStatus,
 	start_date=cast(updateStartDate as date),
 	due_date=cast(updateDueDate as date),
 	assign_employee_id=updateAssignEmployeeId,
 	updated_by=inputUpdatedBy,
 	updated_date=cast(inputUpdatedDate as date)
 where id=taskId;
END;
$$;