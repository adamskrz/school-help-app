import sqlite3


def AllTasks(dbpath):
    connection = sqlite3.connect(dbpath, isolation_level=None)
    cursor = connection.cursor()
    sql_command = """SELECT * FROM homework;"""
    cursor.execute(sql_command)
    
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
        for row in cursor.fetchall()]

    cursor.close()
    return data

if __name__ == "__main__":
    result = AllTasks('homework.db')
    print(result)
