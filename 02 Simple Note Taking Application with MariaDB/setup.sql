CREATE DATABASE IF NOT EXISTS taskapp;

CREATE TABLE IF NOT EXISTS taskapp.category(
    category_id INT(2) NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(15) NOT NULL,
    category_desc VARCHAR(30),
    CONSTRAINT category_category_id_pk PRIMARY KEY(category_id),
    CONSTRAINT category_category_name_uk UNIQUE(category_name)
);

/*Creates task table*/
CREATE TABLE IF NOT EXISTS taskapp.task(
    task_id INT(3) NOT NULL AUTO_INCREMENT,
    task_name VARCHAR(20) NOT NULL,
    task_details VARCHAR(50),
    date_added DATE DEFAULT CURDATE(),
    task_deadline DATE,
    task_status VARCHAR(10) DEFAULT "Unfinished",
    category_id INT(2),
    CONSTRAINT task_task_id_pk PRIMARY KEY(task_id),
    CONSTRAINT task_category_id_fk FOREIGN KEY(category_id) REFERENCES category(category_id)
);

CREATE USER IF NOT EXISTS 'pythonapp'@'127.0.0.1'
   IDENTIFIED BY 'sirperic0';

GRANT SELECT, INSERT, UPDATE, DELETE, DROP
   ON taskapp.category
   TO 'pythonapp'@'127.0.0.1';

GRANT SELECT, INSERT, UPDATE, DELETE, DROP
   ON taskapp.task
   TO 'pythonapp'@'127.0.0.1';