CREATE TABLE IF NOT EXISTS tbl_employee(
                id Integer Primary Key,
                name text not null,
                username text not null unique,
                password text not null
            );
			
SELECT * FROM tbl_employee
			
INSERT INTO tbl_employee(id,name,username,password)
VALUES
(1,'THAI','thai','12345'),
(2,'SILA','sila','12345'),
(3,'BUNTEUN','bunteun','12345'),
(4,'VOTHY','vothy','12345')