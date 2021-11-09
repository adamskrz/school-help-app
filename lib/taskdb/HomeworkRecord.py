import sqlite3

def InsertHW(dbpath,taskName, dueDate, subject, issueDate = '', taskType = '', description = ''):
    connection = sqlite3.connect(dbpath, isolation_level=None)
    cursor = connection.cursor()
    format_str = """INSERT INTO homework (taskID, taskName, dueDate, subject, issueDate, taskType, description, done)
    VALUES (NULL, '{task}', '{due}', '{DBsubject}', '{issue}', '{type}', '{des}', False);"""
    sql_command = format_str.format(task = taskName, due = dueDate, DBsubject = subject, issue = issueDate, type = taskType, des = description)
    #print(sql_command)
    cursor.execute(sql_command)
    id = cursor.lastrowid
    cursor.close()
    return id


if __name__ == "__main__":
    print(InsertHW('homework.db',"Ex3A", "2020-02-13", "Maths", "2020-01-23", "project"))
    connection = sqlite3.connect("homework.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM homework") 
    desc = cursor.description
    column_names = [col[0] for col in desc]
    result = [dict(zip(column_names, row))
        for row in cursor.fetchall()]
    print(result)