import sqlite3


def SubjectList(dbpath):
    subject_list = []
    connection = sqlite3.connect(dbpath, isolation_level=None)
    connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    sql_command = """SELECT subject FROM homework;"""
    cursor.execute(sql_command)
    data = cursor.fetchall()
    cursor.close()
    for subject in data:
        if subject not in subject_list:
            subject_list.append(subject)

    return subject_list
    

if __name__ == "__main__":
    result = SubjectList('homework.db')
    print(result)