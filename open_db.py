#!/home/workivan/PythonCode/Birthdays_venv_vers_3_bd/venv/bin/python3

import sqlite3
from pathlib import Path

DB_BIRTHDAYS = Path('/home/workivan/PythonCode/PUT_IN_GIT/birthdays.db')


def connecting_to_database():
    with sqlite3.connect(DB_BIRTHDAYS) as conn:
        return conn


def create_new_table(connecting):
    with connecting:
        cursor = connecting.cursor()
        sql_request = """CREATE TABLE IF NOT EXISTS birthday_people (
            id integer PRIMARY KEY,
            fio text NOT NULL,
            date integer,
            month integer,
            year integer
        );"""
        cursor.execute(sql_request)

# ! добавление одного значения в таблицу


def add_one_records_to_table(connecting, fio, d, m, y):
    with connecting:
        sql_request = "INSERT INTO birthday_people (fio, date, month, year) VALUES(?, ?, ?, ?)"
        z = (fio, d, m, y)
        connecting.execute(sql_request, z)
        connecting.commit()

def reader_table(connecting):
    with connecting:
        sql_request = "SELECT * FROM birthday_people"
        cursor = connecting.execute(sql_request)
        records = cursor.fetchall()
        return records


def update_value_table(connecting, fio, d, m, y, edit_id):
    with connecting:
        sql_request = "SELECT * FROM birthday_people"
        cursor = connecting.execute(sql_request)
        cursor.execute('''UPDATE birthday_people
         SET fio = ?, date=?, month=?, year=?
         WHERE id == ?''',
                       (fio, d, m, y, edit_id))
        connecting.commit()


def delete_value_table(connecting, edit_id):
    with connecting:
        sql_request = "SELECT * FROM birthday_people"
        cursor = connecting.execute(sql_request)
        cursor.execute('''DELETE FROM birthday_people
         WHERE id == ?''',
                       (edit_id,))
        connecting.commit()

# ?-----------------------------   dates  ------------------------------------------')


def create_new_table_dates(connecting):
    with connecting:
        cursor = connecting.cursor()
        sql_request = """CREATE TABLE IF NOT EXISTS significant_dates (
            id integer PRIMARY KEY,
            date integer,
            month integer,
            event text NOT NULL
        );"""
        cursor.execute(sql_request)


def add_records_to_table_dates(connecting, information):
    with connecting:
        sql_request = "INSERT INTO significant_dates (date, month, event) VALUES(?, ?, ?)"
        for k, v in information.items():
            d, m = int(k[:2]), int(k[2:4])
            z = (d, m, v)
            connecting.execute(sql_request, z)
            connecting.commit()


# ! добавл одного знач в таблицу
def add_one_records_to_table_dates(connecting, d, m, v):
    with connecting:
        sql_request = "INSERT INTO significant_dates (date, month, event) VALUES(?, ?, ?)"
        z = (d, m, v)
        connecting.execute(sql_request, z)
        connecting.commit()


def reader_table_dates(connecting):
    with connecting:
        sql_request = "SELECT * FROM significant_dates"
        cursor = connecting.execute(sql_request)
        records = cursor.fetchall()
        return records


def reader_table_dates_id(connecting, id):  # ! чтение выборки по id
    with connecting:
        cur = connecting.cursor()
        cur.execute('''SELECT * FROM significant_dates
        WHERE id == ?''',
                    (id,))
        x = cur.fetchone()
        return x[0]


def reader_table_dates_month(connecting, m):  # ! чтение выборки по месяцам
    my_list = []
    with connecting:
        cur = connecting.cursor()
        cur.execute('''SELECT * FROM significant_dates
        WHERE month == ?''',
                    (m,))
        records = cur.fetchall()
        for x in records:
            z = f'id:{x[0]:<5} {x[1]}.{x[2]}  {x[3]}'
            my_list.append(z)
        return my_list


# ! чтение выборки по дню и месяцу
def reader_table_dates_day_month(connecting, d, m):
    my_list = []
    with connecting:
        cur = connecting.cursor()
        cur.execute('''SELECT * FROM significant_dates
        WHERE date == ? AND month == ?''',
                    (d, m,))
        records = cur.fetchall()
        for x in records:
            z = f'id:{x[0]:<5} {x[1]}.{x[2]}  {x[3]}'
            my_list.append(z)
        return my_list


def reader_table_dates_name(connecting, value):  # ! чтение выборки по названию
    my_list = []
    with connecting:
        cur = connecting.cursor()
        cur.execute('''SELECT * FROM significant_dates
         WHERE event LIKE  ? OR event  LIKE ? OR event  LIKE ?''',
                    (value+'%', '%'+value, '%'+value+'%',))
        records = cur.fetchall()
        for x in records:
            z = f'id:{x[0]:<5} {x[1]}.{x[2]}  {x[3]}'
            my_list.append(z)
        return my_list


def delete_value_table_dates_all(connecting):
    with connecting:
        cur = connecting.cursor()
        cur.execute("DELETE FROM significant_dates")
        connecting.commit()


def delete_value_table_dates_id(connecting, id_dates):
    with connecting:
        sql_request = "SELECT * FROM significant_dates"
        cursor = connecting.execute(sql_request)
        cursor.execute('''DELETE FROM significant_dates
         WHERE id == ?''',
                       (id_dates,))
        connecting.commit()

# ?-------------------------------------- task ------------------------------------
def create_new_table_task(connecting):  # ! созд таблицу задач
    with connecting:
        cursor = connecting.cursor()
        sql_request = """CREATE TABLE IF NOT EXISTS homework_tasks (
            id integer PRIMARY KEY,
            date text,
            month text,
            year text,
            day_of_week text,
            hour text,
            minute text,
            task text NOT NULL
        );"""
        cursor.execute(sql_request)


def del_table(connecting):  # ! удаление конкретной таблицы
    cursor = connecting.cursor()
    cursor.execute('DROP TABLE homework_tasks')


def add_records_to_table_task(connecting, date, month, year, day_of_week, hour, minute, task):
    with connecting:
        sql_request = "INSERT INTO homework_tasks (date, month, year, day_of_week, hour, minute, task) VALUES(?, ?, ?, ?, ?, ?, ?)"
        z = (date, month, year, day_of_week, hour, minute, task)
        connecting.execute(sql_request, z)
        connecting.commit()

def reader_table_task(connecting):
    with connecting:
        sql_request = "SELECT * FROM homework_tasks"
        cursor = connecting.execute(sql_request)
        records = cursor.fetchall()
        return records
        # print(records)

def delete_value_table_task_id(connecting, id_dates):
    with connecting:
        sql_request = "SELECT * FROM significant_dates"
        cursor = connecting.execute(sql_request)
        cursor.execute('''DELETE FROM homework_tasks
        WHERE id== ?''',
                    (id_dates,))
        connecting.commit()

def reader_table_task_id(connecting, id):  # ! чтение выборки по id
    with connecting:
        cur = connecting.cursor()
        cur.execute('''SELECT * FROM homework_tasks
        WHERE id == ?''',
                    (id,))
        x = str(cur.fetchone())
        return x
    
# if __name__ == '__main__':
#     print((DB_BIRTHDAYS))
#     reader_table_task(connecting_to_database())
    # delete_value_table_task_id(connecting_to_database(), id_dates)
    # add_records_to_table_task(connecting_to_database(), date, month, year, day_of_week, hour, minute, task)
    # del_table(connecting_to_database())
    # create_new_table_task(connecting_to_database())
    # reader_table_task_id(connecting_to_database(), id)

    # create_new_table(connecting_to_database())
    # add_records_to_table(connecting_to_database(), 'events.txt')
    # add_records_to_table(connecting_to_database())
    # reader_table(connecting_to_database())

    # create_new_table_dates(connecting_to_database())
    # add_records_to_table_dates(connecting_to_database(), my_dates)
    # reader_table_dates(connecting_to_database())
    # reader_table_dates_id(connecting_to_database(), id)
    # reader_table_dates_month(connecting_to_database(), m)
    # reader_table_dates_day_month(connecting_to_database(), d, m)
    # reader_table_dates_name(connecting_to_database(), value)
    # delete_value_table_dates_all(connecting_to_database())
    # delete_value_table_dates_id(connecting_to_database(), id_dates)
