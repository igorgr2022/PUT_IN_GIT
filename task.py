#!/home/workivan/PythonCode/Birthdays_venv_vers_3_bd/venv/bin/python3

from open_db import connecting_to_database, reader_table_task
import re
from datetime import datetime
import math

reg_d_m_y = "^(\d{1,2}\.){2}\d{4}"  # ? ищем дату  "01.01.2023"
# ? ищем "(пн, ср, пт)"
reg_weekday = "^\(((пн)|(вт)|(ср)|(чт)|(пт)|(сб)|(вс)|[,]|[\s]){1,19}\)"

shortening_days_of_week = {
    "Mon": "пн",
    "Tue": "вт",
    "Wed": "ср",
    "Thu": "чт",
    "Fri": "пт",
    "Sat": "сб",
    "Sun": "вс"
}


val = ""
day = datetime.now()
current_date = day.strftime("%d.%m.%Y")  # ! находим тек дату
current_day_of_week = day.strftime("%a")  # ! находим тек день недели
for k, v in shortening_days_of_week.items():
    if k == current_day_of_week:
        val = v  # ? присваиваем "val" тек знач дня недели
reg_val = f"({val})"


# def days_before_a_certain_date(): #! сколько  дней до определенной даты
#     # ? задаем дату, до которой нужно посчитать кол-во дней
#     date_str = '2023-06-26'
#     end_date = datetime.strptime(date_str, '%Y-%m-%d')

#     today = datetime.today()
#     difference_in_days = (end_date - today).days
#     if difference_in_days == 0:
#         return 'День приезда Ярика!!!'
#     return f'Осталось {difference_in_days} дней до приезда Ярика из армии!!!'

#! преобразователь инф в норм вид без лишн пробелов
def reader_task_save_to_list():
    dates = reader_table_task(connecting_to_database())
    my_dict = {}
    for z in dates:
        date = z[1]
        if not date == "":
            str_date = [str(z[1]), str(z[2]), str(z[3])]
            date = ".".join(str_date)
        else:
            date = ""
        day_of_week = z[4]
        if not day_of_week == "":
            day_of_week = (f'({z[4]})')
        time = z[5]
        if not time == "":
            str_time = [str(z[5]), str(z[6])]
            time = ":".join(str_time)
        task = z[7]
        all_var = f'{date} {day_of_week} {time} {task}'
        all_var = ' '.join(all_var.split())  # ? убр из стр пуст симв
        my_dict[z[0]] = all_var
    return my_dict


def reader_task_join(value=1, my_dict=reader_task_save_to_list()):
    my_list, my_list_id = [], []
    if value == 1:
        for k in my_dict.keys():
            my_list_id.append(k)
        return my_list_id
    elif value == 2:
        for v in my_dict.values():
            my_list.append(v)
        return ('\n\n').join(my_list)
    else:
        for v in my_dict.values():
            my_list.append(v)
        return my_list

#! сохр меропр в словари по тек дате, дню недели, и остальные меропр
def duration_of_the_event():
    my_dict = reader_task_save_to_list()
    my_dict_id, my_dict_id_others = {}, {}
    for k, v in my_dict.items():
        d_m_y = re.search(reg_d_m_y, v)  # ? наход совпад с датой
        weekday = re.search(reg_weekday, v)  # ? наход совпад c днями недели
        if not d_m_y == None and d_m_y.group() == current_date:
            my_dict_id[k] = v
        elif not weekday == None:
            # ? наход совпад c тек днем недели
            reg_val_ok = re.search(reg_val, weekday.group())
            if not reg_val_ok == None:
                my_dict_id[k] = v
            else:
                my_dict_id_others[k] = v
        else:
            my_dict_id_others[k] = v
    return my_dict_id, my_dict_id_others


z_0 = reader_task_join(2, duration_of_the_event()[0])  # ? текст текущих задач
z_1 = reader_task_join(2, duration_of_the_event()[1])  # ? текст заплан задач


def string_analysis(arg):  # ! узнаем колич строк в конкр разделе задач
    num_main = 46  # ? кол-во символов в строке
    value_str = 0  # ? счётчик строк
    start = 0
    while True:
        # ? наход индекс переноса строки  = 88
        index_n = arg.find("\n", start)
        if index_n == -1:
            # ? узн кол-во строк в одном абзаце = 2
            y = math.ceil((len(arg) - start) / num_main)
            value_str += y  # ? складываем общее кол-во строк
            break
        else:
            # ? узн кол-во строк в одном абзаце = 2
            y = math.ceil((index_n - start) / num_main)
            start = index_n + 2  # ? с какого символа искать =90
            value_str += y  # ? узн общее кол-во строк
    return value_str


def output_of_lines(): #! вывод строк на 1 и 2 стр фрейма
    str_0 = string_analysis(z_0) #? колич строк в текущ задачах
    str_1 = string_analysis(z_1) #? колич строк в запланир задачах
    # ? общее кол-во строк на фрейме
    sum_lines = str_0 + str_1
    lines_default = 16  # ? кол-во строк по умолч
    if sum_lines <= lines_default:  # ? всех строк <= чем которые по умолч
        return z_1 #? получ len>2
    else:
        if str_1 > str_0:
            #? остаток строк который надо вывести на 1 стр
            remaining_lines = lines_default - str_0  
            num_main = 46  # ? кол-во символов в строке
            value_str = 0  # ? счётчик строк
            start = 0
            while True:
                # ? наход индекс переноса строки "\n"
                index_n = z_1.find("\n", start)
                if index_n == -1:
                    y = math.ceil((len(z_1) - start) / num_main)
                    index_n = len(z_1)
                else:
                    # ? кол-во строк в одной задаче
                    y = math.ceil((index_n - start) / num_main)
                value_str += y  # ? всего строк
                if value_str >= remaining_lines:
                    str_lines_1 = z_1[:index_n] #? вывод строк на 1 стр                     
                    str_lines_2 = z_1[index_n+1:] #? вывод строк на 2 стр
                    break
                else:
                    start = index_n + 2  # ? с какого индекса искать =90
            if not len(str_lines_2) == 0:
                return str_lines_1, str_lines_2 #? получ len==2
            else:
                return str_lines_1
