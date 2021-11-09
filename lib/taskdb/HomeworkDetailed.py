import sqlite3

def DetailedInfo(dbpath,taskID):
    connection = sqlite3.connect(dbpath, isolation_level=None)
    cursor = connection.cursor()
    format_str = """SELECT * FROM homework WHERE taskID = {ID};"""
    sql_command = format_str.format(ID = taskID)
    cursor.execute(sql_command)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    result = dict(zip(column_names, cursor.fetchone()))
    
    cursor.close()
    return result


if __name__ == "__main__":
    result = DetailedInfo('homework.db','1')
    print(result)


