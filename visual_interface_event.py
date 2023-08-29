#!/home/workivan/PythonCode/Birthdays_venv_vers_3_bd/venv/bin/python3

from tkinter import *
from events import birthday, full_date, day_week, birthday_tomorrow, events_db
from dates import holidays, holidays_in_few_days
from task import *
import datetime
import re
from pathlib import Path
from open_db import *

Path_Music = Path(
    '/home/workivan/PythonCode/PUT_IN_GIT/music/festive march.mp3')

root = Tk()
root.title("Праздники и дни рождения родственников")
root.geometry('1200x800')
root.resizable(width=False, height=False)


#!Меню"
mainmenu = Menu(root)
root.config(menu=mainmenu)

root.bind('<Escape>', lambda x: root.destroy())  # ! закрытие основного окна

# * проверка на валидность(3 слова+ цифры)
reg_word = r'(^[А-Я][а-я]{3,}\s[А-Я][а-я]{2,}\s[А-Я][а-я]{3,}\s(\d{1,2}\.){2}[1,2][0,9]\d\d$)'
# * проверка ввода дня и месяца 12.04 или 4.6 и т.д.
reg_d_m = r'(^\d{1,2}\.\d{1,2}$)'
# * проверка ввода дня, месяца и года 12.04.2029 до 2029 года
reg_d_m_y = r'(^((0[1-9])|([1-2]\d)|(3[0-1]))\.((0[1-9])|([1][0-2]))\.((202)[3-9])$)'
# * проверка ввода времени 11:30
reg_h_m = r'(^((0[1-9])|(1\d)|(2[0-4]))\:((0\d)|([1-5]\d))$)'


def look_up(numb_z=1):  # ! поиск именинника
    # todo средний левый фрейм перекрывает верхн и нижн левые фреймы
    updating_birthday_label(2)
    frame_left_middle = Frame(
        root, bg='sky blue', relief='ridge', borderwidth=5)
    frame_left_middle.place(relx=0.01, rely=0.01,
                            relwidth=0.55, relheight=0.91)

    # todo поле поиск по ФИО
    def field_name(numb_z):
        if numb_z == 1:
            z = "Поиск или добавление именинника"
            text_look_up_1 = "Внимание! ФИО вводим в родительном падеже: Иванова Ивана Ивановича"
            text_look_up_2 = "Добавить:   Иванову Ивану Ивановичу 01.01.2023"
        elif numb_z == 2:
            z = "Изменить данные именинника"
            text_look_up_1 = "Вводим данные в родительном падеже.  Нажимаем изменить и осуществляем корректировку"
            text_look_up_2 = ""
        elif numb_z == 3:
            z = "Удаление данных"
            text_look_up_1 = "Вводим данные лица, которое хотим удалить."
            text_look_up_2 = "Нажимаем удалить. Затем закрыть."
        label_look_up = Label(frame_left_middle, text=z,
                              font=("Times", 16), padx=5, relief='sunken')
        label_look_up.pack()

        text_look_up = (f'{text_look_up_1}\n{text_look_up_2}')
        focus_look_up = Label(frame_left_middle, text=text_look_up, font=("Comic Sans MS", 13, 'italic'), fg='#BF3030', bg='sky blue',
                              padx=5, wraplength=600, justify=LEFT)
        focus_look_up.place(x=15, y=40)

    field_name(numb_z)

    data_entry_look_up = Label(frame_left_middle, text="Введите данные", font=14,
                               padx=5)
    data_entry_look_up.place(x=15, y=95)

    data_output_look_up = Entry(frame_left_middle, fg="green", width=45)
    data_output_look_up.place(x=220, y=95)

    global lbl_full_look_up
    lbl_full_look_up = Label(frame_left_middle, bg='sky blue',
                             font=("Times", 10), text='', justify=LEFT)  # ? выводит найденные слова
    lbl_full_look_up.place(x=20, y=175)

    def word_search():  # ! поиск слова
        global lbl_full_look_up
        lbl_full_look_up.place_forget()
        data = data_output_look_up.get()  # ? получаем вводимые данные

        if data != "":
            full_look_up = ('\n').join(events_db(data))
            lbl_full_look_up = Label(frame_left_middle, text=full_look_up, bg='sky blue',
                                     font=("Times", 10), justify=LEFT)  # ? выводит найденные слова
            lbl_full_look_up.place(x=20, y=175)

    def clear_look_up():  # ! очистка формы
        try:
            lbl_full_look_up.place_forget()
        except NameError:
            print('Ай яй яй, опять не нашел lbl_full_look_up. Хорошо. Работаем без него!')
        data_output_look_up.delete(0, END)

    def add():  # ! добавить данные именинника
        data = data_output_look_up.get()  # ? получаем инф о новом имениннике
        result = re.match(reg_word, data)
        # ? список именинников из базы данных
        # ? проверка на совпадение данных именинников
        for x in reader_table(connecting_to_database()):
            x_str = f"{x[1]} {x[2]}.{x[3]}.{x[4]}"
            if data in x_str:
                data_output_look_up.insert(0, 'Данные уже ранее были введены!')
                return
        if result == None:
            data_output_look_up.insert(0, 'Введены некорректные данные:   ')
            return
        # ? удал крайние пробелы и разделяем строку по пробелам
        add_value = data.strip().split()
        fio = f"{add_value[0]} {add_value[1]} {add_value[2]}"
        # ? выводим блок с цифрами и раздел их по точке
        number_value = add_value[3].split(".")
        d = int(number_value[0])
        m = int(number_value[1])
        y = int(number_value[2])
        if d > 31 or m > 12:
            data_output_look_up.insert(
                0, 'Введены некорректные данные дня или месяца!  ')
            return
        add_one_records_to_table(
            connecting_to_database(), fio, d, m, y)  # ? сохр в БД
        data_output_look_up.delete(0, END)

    def edit():  # ! изменить данные именинника (нажали на кнопку)
        data = data_output_look_up.get()  # ? данные, которые надо изменить
        # ? проверка на совпадение с БД
        for x in reader_table(connecting_to_database()):
            x_str = f"{x[1]} {x[2]}.{x[3]}.{x[4]}"
            if data == x_str:
                edit_id = x[0]  # ? id данных чел. для изменения
                lbl_full_look_up.place_forget()  # ? скрываю поле с инф о найденных лицах
                change_to = Label(frame_left_middle, bg='sky blue', text="заменить на", font=14,
                                  padx=5)
                change_to.place(x=15, y=200)
                global new_data
                new_data = Entry(frame_left_middle, fg="green", width=45)
                new_data.place(x=220, y=200)

                def save():  # ! сохр новые изменения
                    data_1 = new_data.get()  # ? данные нового лица
                    # ? проверяем на правильность ввода данных
                    result = re.match(reg_word, data_1)
                    if result == None:
                        new_data.insert(0, 'Введены некорректные данные:   ')
                        return
                    # ? проверка на совпадение данных именинников
                    for x in reader_table(connecting_to_database()):
                        x_str = f"{x[1]} {x[2]}.{x[3]}.{x[4]}"
                        if data_1.strip() == x_str.strip():
                            new_data.insert(
                                0, 'Данные уже ранее были введены!   ')
                            return
                    # ? удал крайние пробелы и разделяем строку по пробелам
                    add_value = data_1.strip().split()
                    fio = f"{add_value[0]} {add_value[1]} {add_value[2]}"
                    # ? выводим блок с цифрами и раздел их по точке
                    number_value = add_value[3].split(".")
                    d = int(number_value[0])
                    m = int(number_value[1])
                    y = int(number_value[2])
                    if d > 31 or m > 12:
                        data_output_look_up.insert(
                            0, 'Введены некорректные данные дня или месяца!  ')
                        return
                    # ? обновл данные в БД
                    update_value_table(
                        connecting_to_database(), fio, d, m, y, edit_id)
                    new_data.delete(0, END)

                def clear_entry():
                    new_data.delete(0, END)

                save_new_data = Button(frame_left_middle, text='Сохранить',
                                       font=("Arial", 10, 'bold'), command=save)
                save_new_data.place(x=420, y=235)

                clear_new_data = Button(frame_left_middle, text='Очистить поле',
                                        font=("Arial", 10, 'bold'), command=clear_entry)
                clear_new_data.place(x=260, y=235)

    def close_look_up():  # ! закрыть форму
        frame_left_middle.place_forget()
        updating_birthday_label(1)

    def del_data():  # ! удалить данные именинника
        data = data_output_look_up.get()  # ? получаем инф об удаляемом
        for x in reader_table(connecting_to_database()):
            x_str = f"{x[1]} {x[2]}.{x[3]}.{x[4]}"
            if data == x_str:  # ? проверка на совпадение данных
                edit_id = x[0]  # ? id чел. для удаления
                delete_value_table(connecting_to_database(), edit_id)
                data_output_look_up.delete(0, END)

    search_data = Button(frame_left_middle, text='Найти',
                         font=("Arial", 10, 'bold'), command=word_search)
    search_data.place(x=220, y=135)

    clear_data = Button(frame_left_middle, text='Очистить',
                        font=("Arial", 10, 'bold'), command=clear_look_up)
    clear_data.place(x=310, y=135)

    #! кнопки добавить, изменить, удалить
    if numb_z == 1:
        add_data = Button(frame_left_middle, text='Добавить',
                          font=("Arial", 10, 'bold'), command=add)
        add_data.place(x=420, y=135)
    elif numb_z == 2:
        edit_data = Button(frame_left_middle, text='Изменить',
                           font=("Arial", 10, 'bold'), command=edit)
        edit_data.place(x=420, y=135)
    elif numb_z == 3:
        btn_del_data = Button(frame_left_middle, text='Удалить',
                              font=("Arial", 10, 'bold'), command=del_data)
        btn_del_data.place(x=420, y=135)

    close_data = Button(frame_left_middle, text='Закрыть', fg='#FF4040', font=(
        "Arial", 10, 'bold'), command=close_look_up)
    close_data.place(x=530, y=135)


def change():  # !изменить данные именинника
    look_up(numb_z=2)


def delete_data():  # !удалить данные именинника
    look_up(numb_z=3)


def close_frame():  # ! закр вкладку "созд даты"
    frame_bottom.destroy()  # ? удал фрейм
    updating_label_dates(1)  # ? созд первоначальную вкладку "знам даты"


def create_significant_dates():  # ! созд праздн даты
    updating_label_dates(2)
    lbl_enter_day = Label(frame_bottom, text="Введите день", padx=10, pady=1)
    lbl_enter_day.place(x=10, y=45)
    entry_enter_day = Entry(frame_bottom, fg="green", width=8)
    entry_enter_day.place(x=165, y=45)  # ? поле ввода информ
    entry_enter_day.insert(0, '10')

    lbl_enter_month = Label(frame_bottom, text="Введите месяц", padx=7, pady=1)
    lbl_enter_month.place(x=10, y=75)
    entry_enter_month = Entry(frame_bottom, fg="green", width=8)
    entry_enter_month.place(x=165, y=75)  # ? поле ввода информ
    entry_enter_month.insert(0, '12')

    lbl_enter_name = Label(
        frame_bottom, text="Введите название", padx=7, pady=1)
    lbl_enter_name.place(x=10, y=105)
    entry_enter_name = Entry(frame_bottom, fg="green", width=55)
    entry_enter_name.place(x=165, y=105)  # ? поле ввода информ
    entry_enter_name.insert(0, 'День матери')

    def clear_field():  # ? очищаем введен данные
        entry_enter_day.delete(0, END)
        entry_enter_month.delete(0, END)
        entry_enter_name.delete(0, END)

    def create_dates():
        try:
            d = int(entry_enter_day.get())
        except ValueError:
            entry_enter_day.delete(0, END)
            entry_enter_day.insert(0, 'Ошибка')
            return
        if d > 31:
            entry_enter_day.delete(0, END)
            entry_enter_day.insert(0, 'Ошибка')
            return
        try:
            m = int(entry_enter_month.get())
        except ValueError:
            entry_enter_month.delete(0, END)
            entry_enter_month.insert(0, 'Ошибка')
            return
        if m > 12:
            entry_enter_month.delete(0, END)
            entry_enter_month.insert(0, 'Ошибка')
            return
        v = entry_enter_name.get()
        if v == "":
            entry_enter_name.delete(0, END)
            entry_enter_name.insert(0, 'Ошибка')
            return
        add_one_records_to_table_dates(
            connecting_to_database(), d, m, v)  # ?сохр праздн даты
        clear_field()

    btn_clear_field = Button(frame_bottom, text='Очистить',
                             font=("Arial", 10, 'bold'), command=clear_field)
    btn_clear_field.place(x=165, y=140)
    btn_create_dates = Button(frame_bottom, text='Сохранить',
                              font=("Arial", 10, 'bold'), command=create_dates)
    btn_create_dates.place(x=270, y=140)
    btn_close_frame = Button(frame_bottom, text='Закрыть',
                             font=("Arial", 10, 'bold'), command=close_frame)
    btn_close_frame.place(x=385, y=140)


def delete_significant_dates():  # ! удаление праздн даты
    updating_label_dates(3)
    text_del_1 = 'В запрос вводим либо дату: 12.4, либо месяц: 4 или название: день космонавтики,'
    text_del_2 = 'при чем регистр слов имеет значение, т.е "День" или "день" выдадут разные результаты.'
    text_del = f"{text_del_1}\n{text_del_2}"
    attention_before_deleting = Label(frame_bottom, text=text_del, font=("Comic Sans MS", 13, 'italic'), fg='#BF3030', bg='sky blue',
                                      padx=5, wraplength=600, justify=LEFT)
    attention_before_deleting.place(x=15, y=35)

    attention_request = Label(
        frame_bottom, text="Введите запрос", font=14, padx=5)
    attention_request.place(x=15, y=80)

    entering_request = Entry(frame_bottom, fg="green", width=45)
    entering_request.place(x=180, y=80)

    entry_delete_id = Entry(frame_bottom, fg="red", width=45)
    entry_delete_id.place(x=105, y=150)  # ? поле ввода информ
    entry_delete_id.insert(0, 'Введите № id для удаления')

    def find_dsd():
        global lb_selection_field
        checking_data = entering_request.get()
        dd = len(checking_data)

        # ?проверяем совпад на день и месяц
        d_m = re.search(reg_d_m, checking_data)
        if checking_data == "":
            return
        elif dd < 3 and checking_data.isdigit():  # ?проверка на ввод месяца
            m = int(checking_data)
            if m > 12:
                entering_request.insert(
                    0, 'Месяц не может быть больше 12     ')
                return
            try:
                lb_selection_field.destroy()
            except NameError:
                print('Ой не могу найти lb_selection_field')
            text = ('\n').join(reader_table_dates_month(
                connecting_to_database(), m))
        elif d_m != None:  # ?проверка на ввод дня и месяца
            v = checking_data.split('.')
            d1, m1 = int(v[0]), int(v[1])
            if d1 > 31 or m1 > 12:
                entering_request.insert(
                    0, 'Превышены значения дня или месяца     ')
                return
            try:
                lb_selection_field.destroy()
            except NameError:
                print('Ой не могу найти lb_selection_field')
            text = ('\n').join(reader_table_dates_day_month(
                connecting_to_database(), d1, m1))
        else:
            value = checking_data
            try:
                lb_selection_field.destroy()
            except NameError:
                print('Ой не могу найти lb_selection_field')
            text = ('\n').join(reader_table_dates_name(
                connecting_to_database(), value))
        lb_selection_field = Label(frame_bottom, text=text, bg='sky blue',
                                   font=("Times", 10), justify=LEFT)
        lb_selection_field.place(x=15, y=175)

    def clear_dsd():
        entering_request.delete(0, END)
        lb_selection_field.destroy()

    def delete_id():  # ? нажатие на кнопку Удалить
        id_text = entry_delete_id.get()
        try:  # ? проверка наличия в БД id
            reader_table_dates_id(connecting_to_database(), id_text)
        except TypeError:
            entry_delete_id.delete(0, END)
            entry_delete_id.insert(0, f'id:{id_text} в базе отсутствует')
            return

        entry_delete_id.delete(0, END)  # ? очищаем поле ввода
        del_text = f"Удалить id:{id_text} ?"
        # ?в поле ввода вносим удаляемый текст
        entry_delete_id.insert(0, del_text)

        def delete_no():
            entry_delete_id.delete(0, END)
            entry_delete_id.insert(0, 'Введите № id для удаления')
            try:
                lb_selection_field.destroy()
            except NameError:
                print('Ой не могу найти lb_selection_field')
            btn_delete_id_yes.destroy()  # ? удаление кнопки ДА
            btn_delete_id_no.destroy()  # ? удаление кнопки НЕТ

        def delete_yes():
            delete_value_table_dates_id(connecting_to_database(), id_text)
            delete_no()  # ? производит очистку поля ввода

        btn_delete_id_yes = Button(frame_bottom, text='ДА', bg='#ff3300',
                                   font=("Arial", 10, 'bold'), command=delete_yes)
        btn_delete_id_yes.place(x=525, y=145)
        btn_delete_id_no = Button(frame_bottom, text='НЕТ',
                                  font=("Arial", 10, 'bold'), command=delete_no)
        btn_delete_id_no.place(x=590, y=145)

    btn_to_find = Button(frame_bottom, text='Найти',
                         font=("Arial", 10, 'bold'), command=find_dsd)
    btn_to_find.place(x=180, y=110)
    btn_clear = Button(frame_bottom, text='Очистить',
                       font=("Arial", 10, 'bold'), command=clear_dsd)
    btn_clear.place(x=260, y=110)
    btn_close_frame = Button(frame_bottom, text='Закрыть',
                             font=("Arial", 10, 'bold'), command=close_frame)
    btn_close_frame.place(x=360, y=110)
    btn_delete_id = Button(frame_bottom, text='Удалить', bg='#ff3300',
                           font=("Arial", 10, 'bold'), command=delete_id)
    btn_delete_id.place(x=15, y=145)


#!-----------------------------------------задачи-------------------------------------
#! ----------------------------------- создать задачу --------------------------------
def create_task():
    update_label_task_text(2)  # ? скрыли инф с задачами
    fr_task_duplicate = Frame(
        bg='sky blue', bd=1, relief='ridge', borderwidth=5)
    fr_task_duplicate.place(relx=0.56, rely=0.01,
                            relwidth=0.43, relheight=0.96)

    Label(fr_task_duplicate, text='Новая задача', font=(
        "Times", 16), padx=5, relief='sunken').pack()

    lbl_help = Label(fr_task_duplicate, text="Информация", padx=3,
                     font=("Times", 14, "bold"), fg='#003B4A', bg='sky blue')
    lbl_help.place(x=195, y=50)
    text_help = 'При вводе данных соблюдаем следующие условия:\nДата:   01.05.2023\n'\
        'Время:   09:08'
    lbl_help_1 = Label(fr_task_duplicate, text=text_help, padx=3,
                       font=("Times", 12), fg='#003B4A', bg='sky blue', justify="left")
    lbl_help_1.place(x=10, y=75)

# ?----------------- Дата ----------------------------------------
    lbl_enter_data_task = Label(
        fr_task_duplicate, text="Дата", bg='sky blue', padx=3)
    lbl_enter_data_task.place(x=10, y=150)
    entry_date_task = Entry(fr_task_duplicate, fg="green", width=10)
    entry_date_task.place(x=130, y=150)  # ? поле ввода информ
    entry_date_task.insert(0, '01.05.2023')
# ?----------------- День недели ----------------------------------------
    lbl_enter_day_of_week = Label(
        fr_task_duplicate, text="День недели", bg='sky blue', padx=3)
    lbl_enter_day_of_week.place(x=10, y=180)

    # ? Фрейм для days_of_week
    fr_days_of_week = Frame(fr_task_duplicate, bg='sky blue', borderwidth=0)
    fr_days_of_week.place(x=130, y=180)

    cb_var = []
    for x in shortening_days_of_week.values():
        var = IntVar()
        Checkbutton(fr_days_of_week, variable=var,
                    text=x, bg='sky blue').pack(side=LEFT)
        cb_var.append(var)

# ?----------------- Время ----------------------------------------
    lbl_enter_time_task = Label(
        fr_task_duplicate, text="Время", bg='sky blue', padx=3)
    lbl_enter_time_task.place(x=10, y=210)
    entry_time_task = Entry(fr_task_duplicate, fg="green", width=5)
    entry_time_task.place(x=130, y=210)
    entry_time_task.insert(0, '11:30')
# ?----------------- Задача ----------------------------------------
    lbl_enter_task = Label(fr_task_duplicate, text="Задача",
                           bg='sky blue', padx=3)
    lbl_enter_task.place(x=10, y=240)
    entry_task = Entry(fr_task_duplicate, fg="green", width=45)
    entry_task.place(x=130, y=240)
    entry_task.insert(0, 'Найти интересную работу')

    def task_del():  # ! очищаем поля ввода
        entry_date_task.delete(0, END)
        entry_time_task.delete(0, END)
        entry_task.delete(0, END)
        for x in cb_var:
            x.set(0)

    def task_save():  # ! сохраняем введенные данные в БД
        def frame_attention(text):  # ?созд фрейм для вывода дополн информации
            fr_attention = Frame(fr_task_duplicate, bg='#7EC3DE',
                                 relief='raised', borderwidth=1)
            fr_attention.place(x=50, y=320, relwidth=0.85, relheight=0.15)
            lbl_attention = Label(
                fr_attention,  bg='#7EC3DE', fg='#8E0000', text=text, font=("Times", 14), padx=5)
            lbl_attention.pack()
            Button(fr_attention, text='Закрыть',
                   command=fr_attention.destroy).place(x=175, y=70)

        date_1 = entry_date_task.get()  # todo дата
        time_1 = entry_time_task.get()  # todo время
        task_1 = entry_task.get()  # todo задача
        days_of_week_1 = []  # todo день недели
        for text, var in zip(shortening_days_of_week.values(), cb_var):
            if var.get():
                days_of_week_1.append(text)
        if len(days_of_week_1) == 0:
            days_of_week_1 = ""
        else:
            # ? преобразуем список в строку
            days_of_week_1 = ', '.join(days_of_week_1)
        #!-------проверки--------------------------------------
        if not date_1 == "":
            # ?проверяем совпад день, месяц и год
            d_m_y = re.search(reg_d_m_y, date_1)
            if d_m_y == None:
                frame_attention('\nВведена не корректная дата')
                return
            else:
                z = date_1.split('.')  # todo преобразуем дату в отд эл-ты
                date, month, year = z[0], z[1], z[2]
        else:
            date, month, year, d_m_y = "", "", "", ""

        if not time_1 == "":     # ? проверка ввода времени 11:30
            h_m = re.search(reg_h_m, time_1)
            if h_m == None:
                frame_attention('\nВведено не корректное значение времени')
                return
            else:
                t = time_1.split(':')
                hour, minute = t[0], t[1]
        else:
            hour, minute, h_m = "", "", ""
        if date_1 and days_of_week_1:
            frame_attention('\nЗаполняется либо дата либо день недели!')
            return
        elif task_1 == "":
            frame_attention('\nЗаполните поле задача!')
            return

        add_records_to_table_task(connecting_to_database(
        ), date, month, year, days_of_week_1, hour, minute, task_1)

        if len(task_1) > 43:  # ? чтобы текст в фрейме frame_attention обрезался аккуратно
            task_2 = f'{task_1[:43]}...'
            frame_attention(f'\nСОХРАНЕНА ЗАДАЧА\n {task_2}')
        else:
            frame_attention(f'\nСОХРАНЕНА ЗАДАЧА\n {task_1}')
        # ? сброс полей ввода информации
        entry_date_task.delete(0, END)
        entry_time_task.delete(0, END)
        entry_task.delete(0, END)
        for z in cb_var:
            z.set(0)

    def close_menu():  # ! скрываем виджет создания задачи
        fr_task_duplicate.place_forget()
        update_label_task_text(1)  # ? восстанавливаем фрейм с задачами

    Button(fr_task_duplicate, text='Удалить', font=(
        "Arial", 9, 'bold'), command=task_del).place(x=10, y=275)

    Button(fr_task_duplicate, text='Сохранить', font=(
        "Arial", 9, 'bold'), command=task_save).place(x=120, y=275)

    Button(fr_task_duplicate, text='Закрыть', font=(
        "Arial", 9, 'bold'), command=close_menu).place(x=240, y=275)


def deleting_a_task():  # ! ------------Раздел - удалить задачу--------------
    update_label_task_text(2)  # ? убираем фрейм
    fr_task_checkbutton = Frame(root, bg='sky blue')  # ? Фрейм для checkbutton
    fr_task_checkbutton.place(relx=0.565, rely=0.015,
                              relwidth=0.421, relheight=0.944)
    lbl_task_checkbutton = Label(fr_task_checkbutton, text='Удаление задач', font=(
        "Times", 16), padx=5, relief='sunken')
    lbl_task_checkbutton.pack()
    var_task = []
    for x in reader_task_join(3, reader_task_save_to_list()):
        var = IntVar()
        Checkbutton(fr_task_checkbutton, variable=var, text=x, offvalue=0, onvalue=1,  font=("Comic Sans MS", 12),
                    fg='#310062', bg='sky blue', wraplength=460, padx=10, pady=5, justify='left', highlightthickness=0).pack(anchor=W)
        var_task.append(var)

    Label(fr_task_checkbutton, text='Внимание!!!  Галочка - значит удалить задачу.',
          font=("Times", 10), padx=5,  bg='sky blue', fg='red', wraplength=460, justify='left').pack()  # ? Предупр об удал

    def del_checkbutton():  # ! кнопка - удалить конкр задачу
        list_deletes = []
        for i, x in enumerate(var_task):
            if x.get() != 0:  # ? находим  отмеченные галочки
                # ? соотносим индекс удал стр с id удал стр
                y = reader_task_join(1, reader_task_save_to_list())[i]
                list_deletes.append(y)
        for z in list_deletes:
            delete_value_table_task_id(connecting_to_database(), z)
        exit_delete_task()

    def uncheck_the_boxes():  # ! кнопка - установить/снять галочки
        for z in var_task:
            if z.get() == 0:
                z.set(1)
            else:
                z.set(0)

    def exit_delete_task():  # ! кнопка выход из раздела удаления задач
        fr_task_checkbutton.destroy()
        # update_label_task_text(2)  # ? убираем фрейм
        update_label_task_text(1)  # ? восстанавливаем фрейм с задачами

    Button(fr_task_checkbutton, text='Убр/уст галочки',
           command=uncheck_the_boxes).pack(anchor=N, ipadx=3, padx=25, side=LEFT)
    Button(fr_task_checkbutton, text='Удалить задачу',
           command=del_checkbutton).pack(anchor=N, padx=25, side=LEFT)
    Button(fr_task_checkbutton, text='Выход', command=exit_delete_task).pack(
        anchor=N, padx=15, side=LEFT)


# ! ------------МЕНЮ ---------------------------------------------------
birthdaymenu = Menu(mainmenu, tearoff=0)  # todo создание меню дни рождения
mainmenu.add_cascade(label='Дни рождения', menu=birthdaymenu)
birthdaymenu.add_command(label="Найти или добавить", command=look_up)
birthdaymenu.add_command(label="Изменить", command=change)
birthdaymenu.add_command(label="Удалить", command=delete_data)

memorable_date = Menu(mainmenu, tearoff=0)  # todo создание меню Даты
mainmenu.add_cascade(label='Даты', menu=memorable_date)
memorable_date.add_command(label="Создать", command=create_significant_dates)
memorable_date.add_command(label="Удалить", command=delete_significant_dates)

filemenu = Menu(mainmenu, tearoff=0)  # todo создание меню задачи
mainmenu.add_cascade(label='Задачи', menu=filemenu)
filemenu.add_command(label="Создать задачу",  command=create_task)
filemenu.add_command(label="Удалить задачу", command=deleting_a_task)


# todo верхний левый фрейм
frame_top = Frame(root, bg='sky blue', bd=1, relief='ridge', borderwidth=5)
frame_top.place(relx=0.01, rely=0.01, relwidth=0.55, relheight=0.45)


def fr_bottom():  # todo нижний левый фрейм
    global frame_bottom
    frame_bottom = Frame(root, bg='sky blue', bd=1,
                         relief='ridge', borderwidth=5)
    frame_bottom.place(relx=0.01, rely=0.45, relwidth=0.55, relheight=0.47)


# todo фрейм дата, время, день недели
frame_footer1 = Frame(root, bg='sky blue', bd=1, relief='ridge', borderwidth=5)
frame_footer1.place(relx=0.01, rely=0.92, relwidth=0.2, relheight=0.05)
label_footer1 = Label(master=frame_footer1, text=full_date(),
                      bg='sky blue', font=("Arial", 14, 'bold'))
label_footer1.pack()

frame_footer2 = Frame(root, bg='sky blue', bd=1, relief='ridge', borderwidth=5)
frame_footer2.place(relx=0.21, rely=0.92, relwidth=0.25, relheight=0.05)
label_footer2 = Label(master=frame_footer2, text=day_week(),
                      bg='sky blue', font=("Arial", 14, 'bold'))
label_footer2.pack()

frame_footer3 = Frame(root, bg='sky blue', bd=1, relief='ridge', borderwidth=5)
frame_footer3.place(relx=0.46, rely=0.92, relwidth=0.1, relheight=0.05)


def tick():  # ! вывод обновляемое время
    label_footer3.after(1000, tick)
    label_footer3['text'] = datetime.datetime.now().strftime("%H:%M:%S")


label_footer3 = Label(master=frame_footer3,  bg='sky blue',
                      font=("Arial", 14, 'bold'))
label_footer3.pack()
tick()

#!--------------------------------------------------------------------- фрейм с задачами
# todo Фрейм с задачами (справа)
fr_task = Frame(bg='sky blue', bd=1, relief='ridge', borderwidth=5)
fr_task.place(relx=0.56, rely=0.01, relwidth=0.43, relheight=0.96)

lbl_task = Label(fr_task, text='Запланированные события',
                 font=("Times", 16), padx=5, relief='sunken').pack()


def updating_birthday_label(x):  # ! скрыть или показать инф с днями рождения
    z = birthday()
    if x == 1:
        global label_top
        label_top = Label(frame_top, text='Дни рождения',
                          font=("Times", 16), padx=5, relief='sunken')
        label_top.pack()

        # todo поле дни рождения
        global label_today_birthday_text

        if not len(z) == 0:
            label_today_birthday_text = Label(frame_top, text=z, fg='brown', bg='sky blue',  pady=15, width=63, anchor='w',
                                              font=("Comic Sans MS", 16, 'bold'), justify='left')
            label_today_birthday_text.pack()
            import pygame.mixer as pyg_mix  # ! проигрывание музыки в ДР
            pyg_mix.init()
            pyg_mix.music.load(Path_Music)
            pyg_mix.music.play()

        # todo поле дни рождения через......
        global label_birthday_text
        label_birthday_text = Label(frame_top, text=birthday_tomorrow(), fg='black', bg='sky blue',  width=63, pady=15,
                                    font=("Comic Sans MS", 16, 'bold'), justify='left', anchor='w', wraplength=600)
        label_birthday_text.pack()

    else:
        if not len(z) == 0:
            label_today_birthday_text.pack_forget()  # ? скрыли инф
        label_top.pack_forget()  # ? скрыли инф
        label_birthday_text.pack_forget()  # ? скрыли инф


updating_birthday_label(1)


def updating_label_dates(x):  # ! скрыть или показать инф по знамен датам
    fr_bottom()  # ? созд основной фрейм
    global label_public_holidays
    z = holidays()
    if x == 1:
        # text = 'Знаменательные даты'
        label_public_holidays = Label(frame_bottom, text='Знаменательные даты', font=(
            "Times", 16), padx=5, relief='sunken')
        label_public_holidays.pack()
        global label_public_holidays_1
        if not len(z) == 0:
            label_public_holidays_1 = Label(frame_bottom, text=z, bg='sky blue', fg='brown', anchor='w', width=450, pady=10,
                                            padx=10, font=("Comic Sans MS", 16, 'bold'), justify='left', wraplength=600)
            label_public_holidays_1.pack()

        global label_public_holidays_2
        label_public_holidays_2 = Label(frame_bottom, text=holidays_in_few_days(), bg='sky blue', fg='black', anchor='w', width=450, pady=10,
                                        padx=10, font=("Comic Sans MS", 16, 'bold'), justify='left', wraplength=600)
        label_public_holidays_2.pack()
    else:
        if x == 2:
            text = 'Создать знаменательную дату'
        else:
            text = 'Удалить знаменательную дату'
        if not len(z) == 0:
            label_public_holidays_1.pack_forget()  # ? скрыли инф
        label_public_holidays.pack_forget()  # ? скрыли инф
        label_public_holidays_2.pack_forget()  # ? скрыли инф
        label_public_holidays = Label(frame_bottom, text=text, font=(
            "Times", 16), padx=5, relief='sunken')
        label_public_holidays.pack()


updating_label_dates(1)


def other_tasks():  # ! созд фрейм для 2 стр задач
    # todo Фрейм для 2 стр задач (справа)
    global fr_task_next
    fr_task_next = Frame(bg='sky blue')
    fr_task_next.place(relx=0.565, rely=0.05, relwidth=0.42, relheight=0.91)

    def close_fr_task_next():  # ! удаляем фрейм для 2 стр задач
        fr_task_next.destroy()

    Button(fr_task_next, text='Назад', command=close_fr_task_next).pack(
        anchor=SE, side=BOTTOM, padx=10, pady=20)
    label_task_text_next = Label(fr_task_next, text=z_2, fg='#310062', bg='sky blue', padx=10, pady=3, width=63,
                                 font=("Comic Sans MS", 16, 'bold'), justify='left', anchor='w', wraplength=460)
    label_task_text_next.pack()  # ? вывод  оставшихся задач


def update_label_task_text(x):  # ! скрыть или показать инф с задачами
    global label_task_text
    global label_task_current_date
    z_0 = reader_task_join(2, duration_of_the_event()[
                           0])  # ? список текущих задач
    z_1 = reader_task_join(2, duration_of_the_event()[
                           1])  # ? список заплан задач
    if x == 1:
        if not len(z_0) == 0:
            label_task_current_date = Label(fr_task, text=z_0, fg='brown', bg='sky blue', padx=10, pady=3, width=63, font=(
                "Comic Sans MS", 16, 'bold'), justify='left', anchor='w', wraplength=460)
            label_task_current_date.pack()
        if len(output_of_lines()) > 2:  # ? список заплан задач
            label_task_text = Label(fr_task, text=z_1, fg='#310062', bg='sky blue', padx=10, pady=3, width=63, font=(
                "Comic Sans MS", 16, 'bold'), justify='left', anchor='w', wraplength=460)
            label_task_text.pack()  # ? вывод задач на экран
        else:
            global z_2
            global btn_next
            z_1 = output_of_lines()[0]
            z_2 = output_of_lines()[1]
            btn_next = Button(fr_task, text='Далее', command=other_tasks)
            btn_next.pack(anchor=SE, side=BOTTOM, padx=10, pady=20)
            label_task_text = Label(fr_task, text=z_1, fg='#310062', bg='sky blue', padx=10, pady=3, width=63, font=(
                "Comic Sans MS", 16, 'bold'), justify='left', anchor='w', wraplength=460)
            label_task_text.pack()  # ? вывод задач на экран
    if x == 2:
        if not len(z_0) == 0:
            label_task_current_date.destroy()
        if len(output_of_lines()) == 2:
            btn_next.destroy()
        label_task_text.destroy()  # ? удалили инф с задачами
        if 'fr_task_next' is globals():
            fr_task_next.destroy()


update_label_task_text(1)
root.mainloop()
