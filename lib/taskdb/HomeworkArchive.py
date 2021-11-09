import sqlite3

def ArchiveTasks(dbpath,searchSubject):
    connection = sqlite3.connect(dbpath, isolation_level=None)
    cursor = connection.cursor()
    format_str = """SELECT taskID, taskName, dueDate, subject, issueDate
    FROM homework
    WHERE subject = "{selectedSubject}";"""
    sql_command = format_str.format(selectedSubject = searchSubject)
    cursor.execute(sql_command)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    result = [dict(zip(column_names, row))
        for row in cursor.fetchall()]
    #result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == "__main__":
    result = ArchiveTasks('homework.db','Maths')
    print(result)

