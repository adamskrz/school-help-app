import sqlite3

def DeleteHW(dbpath, taskID):
    connection = sqlite3.connect(dbpath, isolation_level=None)
    cursor = connection.cursor()
    format_str = """DELETE FROM homework WHERE taskID = {id};"""
    sql_command = format_str.format(id = taskID)
    cursor.execute(sql_command)
    cursor.close()
    return