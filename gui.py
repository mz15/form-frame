# -*- coding: utf-8 -*-
from tkinter import Tk, Frame, Label, Entry, Button
from logic import *

def result_window(event):  # Функция окна результатов
    res_window = Tk()
    res_window.title("Результат операции")
    res_window.minsize(width=300, height=100)

    # TODO Функция проверки и сохранения данных
    result_text = Label(res_window, text='Данные приняты')  # display_label
    result_text.pack()

    # saving_data()

    list_result = []
    for number, line in enumerate(list_form):
        list_result_single = []
        list_result_single.append(list_form[number][0])
        list_result_single.append(globals()['entry%d' % number].get())  # Получение значения из текстового поля
        list_result.append(list_result_single)
        file = 'result.txt'
        with open(file, 'w') as f:
            f.write(str(list_result))

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
    # print('$prefix.name:', line[0]
    # print('Отображаемое имя:', line[1])
    # print('Значение:', line[2])
    # print('Тип:', line[3])

    globals()['label%d' % number] = Label(fields_frame, text=line[1])  # display_label
    globals()['label%d' % number].grid(row=number, column=0, padx=20, pady=5)

    globals()['entry%d' % number] = Entry(fields_frame, width=50, bd=2)  # value
    globals()['entry%d' % number].grid(row=number, column=1, padx=20, pady=5)
    globals()['entry%d' % number].insert(0, line[2])  # Значение по умолчанию (введенное или из базы данных)

    # TODO  проверка ввода на соответствие нужному типу данных
"""
list_result = []
for number, line in enumerate(list_form):
    # print('$prefix.name:', line[0]
    # print('Отображаемое имя:', line[1])
    # print('Значение:', line[2])
    # print('Тип:', line[3])
    list_result.append(globals()['entry%d' % number].get())  # Получение значения из текстового поля

    file = 'result.txt'
    with open(file, 'w') as f:
        f.write(str(list_result))

"""

main_window.mainloop()
