import sqlite3

def UpdateHW(dbpath, taskID, taskName, dueDate, subject, complete, issueDate = '', taskType = '', description = ''):
    connection = sqlite3.connect(dbpath, isolation_level=None)
    cursor = connection.cursor()
    format_str = """UPDATE homework SET taskName = '{task}', dueDate = '{due}', subject = '{DBsubject}', issueDate = '{issue}', taskType = '{type}', description = '{des}', done = {fin} WHERE taskID = {id};"""
    sql_command = format_str.format(task = taskName, due = dueDate, DBsubject = subject, issue = issueDate, type = taskType, des = description, fin = complete, id = taskID)
    cursor.execute(sql_command)
    id = cursor.lastrowid
    cursor.close()
    return id

def SetArchiveHW(dbpath, taskID, complete):
    connection = sqlite3.connect(dbpath, isolation_level=None)
    cursor = connection.cursor()
    format_str = """UPDATE homework SET done = {fin} WHERE taskID = {id};"""
    sql_command = format_str.format(fin = complete, id = taskID)
    cursor.execute(sql_command)
    id = cursor.lastrowid
    cursor.close()
    return id

# if __name__ == "__main__":
#     print(InsertHW('homework.db',"Ex3A", "2020-02-13", "Maths", "2020-01-23", "project"))
#     connection = sqlite3.connect("homework.db")

#     cursor = connection.cursor()

#     cursor.execute("SELECT * FROM homework") 
#     desc = cursor.description
#     column_names = [col[0] for col in desc]
#     result = [dict(zip(column_names, row))
#         for row in cursor.fetchall()]
#     print(result)