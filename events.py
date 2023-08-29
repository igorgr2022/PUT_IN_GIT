#!/home/workivan/PythonCode/Birthdays_venv_vers_2_bd/venv/bin/python3

import datetime
import re
from open_db import *


def events_db(word):  # ! находит заданное слово из БД
    list_reg = []  # ? список найденных значений
    for x in reader_table(connecting_to_database()):
        # ? ищем по заданному тексту информацию
        word_reg = re.search(word, x[1], re.IGNORECASE)
        if word_reg != None:
            list_reg.append(f" {x[1]} {x[2]}.{x[3]}.{x[4]}")
    return list_reg


# ? получаем полную инфу по текущей дате
current_date = str(datetime.datetime.today())
current_year = int(current_date[:4])  # ? текущий год
current_month = int(current_date[5:7])  # ? текущий месяц
current_day = int(current_date[8:10])  # ? текущий день
day_z1 = [1, 21, 31]
day_z2 = [2, 3, 4, 22, 23, 24]


def birthday():  # !вывод дней рождения
    today_birthday = []
    for z in reader_table(connecting_to_database()):
        fio, d, m, y = z[1], z[2], z[3], z[4]
        if d == current_day and m == current_month:  # ? если совпали дата и месяц с текущей датой
            x = current_year - y  # ? разность текущего года и найденного
            text = f"Сегодня {x} годовщина {fio}"
            today_birthday.append(text)
    return ('\n').join(today_birthday)

def birthday_tomorrow():  # ! вывод дней рождений за n количество дней
    my_list = []
    for z in reader_table(connecting_to_database()):
        fio, d, m, y = z[1], z[2], z[3], z[4]
        for x in range(1, 20):  # ? добавляем к текущей дате n дней
            # ? измененная на n дней дата
            changed_date = str(datetime.datetime.today() +
                               datetime.timedelta(days=x))
            c = changed_date.split()
            c = c[0].split('-')
            changed_day = int(c[2])
            changed_month = int(c[1])
            changed_year = int(c[0])
            if day_z1.count(x) > 0:
                day_x = ' день '
            elif day_z2.count(x) > 0:
                day_x = ' дня '
            else:
                day_x = ' дней '
            if d == changed_day and m == changed_month:  # ? если даты совпали
                anniversary = changed_year - y  # ? разность текущего года и года именинника
                text = f"Через {x} {day_x} {anniversary} годовщина ({d}.{m}) {fio}"
                my_list.append(text)
    return "\n".join(my_list)


#!footer
int_month = {
    '01': ' января ',
    '02': ' февраля ',
    '03': ' марта ',
    '04': ' апреля ',
    '05': ' мая ',
    '06': ' июня ',
    '07': ' июля ',
    '08': ' августа ',
    '09': ' сентября ',
    '10': ' октября ',
    '11': ' ноября ',
    '12': ' декабря ',
}
a_week = {
    "Mon": "понедельник",
    "Tue": "вторник",
    "Wed": "среда",
    "Thu": "четверг",
    "Fri": "пятница",
    "Sat": "суббота",
    "Sun": "воскресенье"
}

def full_date(): #! вывод день месяц год
    output_date = current_date[8:10]
    for k, p in int_month.items():
        if current_date[5:7] == k:
            output_date = output_date + p + current_date[:4]
            return output_date

def day_week(): #! вывод день недели
    d1 = (datetime.datetime.today()).strftime("%a")
    for k, ww in a_week.items():
        if d1 == k:
            return ww
