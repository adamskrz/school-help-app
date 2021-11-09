import sqlite3

def createDB(dbpath):
    connection = sqlite3.connect(dbpath)
    cursor = connection.cursor()

    sql_command = """
    CREATE TABLE homework ( 
    taskID INTEGER PRIMARY KEY, 
    taskName VARCHAR(30), 
    dueDate DATE, 
    subject VARCHAR(30), 
    issueDate DATE,
    taskType VARCHAR(15),
    description VARCHAR(500),
    done BOOLEAN);"""

    cursor.execute(sql_command)