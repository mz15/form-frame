# -*- coding: utf-8 -*-
from tkinter import Tk, Frame, Label, Entry, Button
from logic import request_input, create_list_form
# from logic import saving_data

request_input()
list_form = create_list_form()

def saving_data():
    # TODO вынести в logic.py

    list_result = []
    for number, line in enumerate(list_form):
        list_result_single = []
        list_result_single.append(list_form[number][0])
        list_result_single.append(globals()['entry%d' % number].get())  # Получение значения из текстового поля
        list_result.append(list_result_single)
    file = 'result.txt'
    with open(file, 'w') as f:
        f.write(str(list_result))

def result_window(event):  # Функция окна результатов
    res_window = Tk()
    res_window.title("Результат операции")
#    res_window.minsize(width=300, height=100)

    # TODO вынести проверку типа данных в logic.py
    error_number = 1
    for number, line in enumerate(list_form):
        value = globals()['entry%d' % number].get()  # Получение значения из текстового поля

        # Контроль ввода
        try:
            if list_form[number][3] == 'int':
                int(value)
            if list_form[number][3] == 'float':
                float(value)

        except ValueError:
            message_result = str('Данные не приняты.\nСписок ошибок:')
            result_text = Label(res_window, text=message_result)
            result_text.grid(row=0, column=0, padx=20, pady=5)

            # Генерирование списка ошибок:
            message = str(str(error_number) + '. Значение в поле "' + list_form[number][1] +
                          '" не соответствует типу данных "' + list_form[number][3] + '".')

            globals()['error%d' % number] = Label(res_window, text=message)
            globals()['error%d' % number].grid(row=number+1, column=0, padx=20, pady=1)
            error_number += 1

    if error_number == 1:  # Если нет ошибок
        file = 'result.txt'
        message_result = str('Данные приняты и сохранены в файле "' + file + '".')
        result_text = Label(res_window, text=message_result)
        result_text.grid(row=0, column=0, padx=20, pady=25)

    saving_data()

    res_window.mainloop()

main_window = Tk()
main_window.title("Фрейм-анкета")
# main_window.minsize(width=700, height=400)

btn_frame = Frame(main_window)
fields_frame = Frame(main_window)
btn_frame.pack()
fields_frame.pack()

btn = Button(btn_frame,
             text="Принять",  # Надпись на кнопке
             width=20  # Ширина
             # height=3,  # Высота
             # bg = "grey",
             # fg = "blue"  # Цвет фона и надписи
             )
btn.grid(row=0, column=0, padx=0, pady=10)
btn.bind("<Button-1>", result_window)  # Вызов функции по нажатию на кнопку

"""
# Пример: формат, в котором должны быть получены данные для заполнения полей
list_form = [
    ['$O.C', 'Цех', '50', 'int'],
    ['$O.U', 'Участок', '123', 'int']
]
"""
# Создание полей
for number, line in enumerate(list_form):
    globals()['label%d' % number] = Label(fields_frame, text=line[1])  # display_label
    globals()['label%d' % number].grid(row=number, column=0, padx=20, pady=5)

    globals()['entry%d' % number] = Entry(fields_frame, width=50, bd=2)  # value
    globals()['entry%d' % number].grid(row=number, column=1, padx=20, pady=5)
    globals()['entry%d' % number].insert(0, line[2])  # Значение по умолчанию (введенное или из базы данных)

main_window.mainloop()
