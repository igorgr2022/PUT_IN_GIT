#!/home/workivan/PythonCode/Birthdays_venv_vers_3_bd/venv/bin/python3

import datetime
from open_db import *

current_date = str(datetime.datetime.today()) #? получаем полную инфу по текущей дате
current_month = int(current_date[5:7])  # ? текущий месяц
current_day = int(current_date[8:10])  # ? текущий день

day_z1= [1, 21, 31]
day_z2= [2, 3, 4, 22, 23, 24]

#! вывод праздничные даты
def holidays():
    my_list = []
    for x in reader_table_dates(connecting_to_database()):
        d, m, v = int(x[1]), int(x[2]), x[3]
        if d == current_day and m == current_month:  # ? если совпали дата и месяц с текущей датой
            text = f'Сегодня {v}'
            my_list.append(text)
    return ('\n').join(my_list)

def holidays_in_few_days():
    my_list = []
    for x in reader_table_dates(connecting_to_database()):
        d, m, v = int(x[1]), int(x[2]), x[3]
        for z in range(1, 20):
            changed_date= str(datetime.datetime.today() + datetime.timedelta(days=z)) #? добавляем к текущей дате n дней
            c = changed_date.split()
            c = c[0].split('-')
            changed_day = int(c[2])
            changed_month = int(c[1])
            if day_z1.count(z) > 0:
                day_x = ' день '
            elif day_z2.count(z) > 0:
                day_x = ' дня '
            else:
                day_x = ' дней '
            if d == changed_day and m == changed_month:  # ? если даты совпали
                text = f'Через {z} {day_x} ({d}.{m}) {v}' 
                my_list.append(text)
    return ('\n').join(my_list)
