# -*- coding: utf-8 -*-
import re

def request_input():
    database_file = 'database.txt'
    with open(database_file, 'r') as db:
        # Переформатирование базы данных - создание списка списков
        global database, request_list
        database = []
        for line in db:
            database += [re.split('\t', line)]

        # Удаление символов '\n'
        for i in range(len(database)):
            if database[i][-1][-1] == '\n':
                database[i][-1] = database[i][-1][:-1]

    while True:  # Цикл, пока ввод не будет корректен

        # Контроль ввода
        try:
            request = input("""
Введите заявки в формате: $Prefix.Name=Value;
Возможен ввод нескольких заявок сразу.
"""
                            )

            form = re.search(r'(\$[A-Za-z]+.[A-Za-z0-9]+=[A-Za-zА-Яа-яЁё0-9 :?.()]*;)+', request)
            # TODO Исправить регулярное выражение - возможен некорректный ввод после первого триплета
            # TODO Подумать над распознаванием ввода триплетов-фактов и триплетов-целей
            request_form = form.group(0)

            """ Пример запроса:
            $C.IST=;$C.PGS=:;$C.PGS2=Точение;$D.D=:;$D.L=:;$D.MAS=:;$D.OB=;$D.SH=;$Z.L=22.5;$Z.K=:;$Z.STS=:;$Z.TW1= ;
            """

            request_list1 = re.split(';', request_form)
            request_list1.pop()

            request_list = []
            for i in range(len(request_list1)):
                request_list.append(re.split('=', request_list1[i]))

            break

        # Контроль формата
        except AttributeError:
            print('Запрос введен в неверном формате. Повторите ввод.')
            continue

def create_list_form():
    # Создания списка с данными для заполнения полей фрейм-анкеты
    list_form = []
    for a in range(len(database)):
        for b in range(len(request_list)):
            if request_list[b][0] == database[a][0]:
                list_form_single = []
                list_form_single.append(database[a][0])
                list_form_single.append(database[a][1])

                # Проверка Value в заявке
                if request_list[b][1] == ':' or request_list[b][1] == ' ' or request_list[b][1] == '':
                    list_form_single.append(database[a][2])
                else:
                    list_form_single.append(request_list[b][1])

                list_form_single.append(database[a][3])

                if request_list[b][1] == ':':
                    list_form_single.append('*')
                else:
                    list_form_single.append('')

                list_form.append(list_form_single)

    """
    # Пример результата:
    list_form = [
    ['$C.PGS', 'Обрабатываемый материал', 'Сталь', 'string', '*'],
    ['$C.PGS2', 'Способ обработки', 'Фрезерование', 'string', ''],
    ['$D.D', 'Диаметр детали', '', 'float', '*'],
    ['$D.SH', 'Значение шероховатости', '1.25', 'float', ''],
    ['$Z.K', 'Код заготовки', '', 'int', ''],
    ...
    ]
    """

    return list_form

# Сохранение введенных значений в текстовых полях фрейм-анкеты
def saving_data():
    list_result = []
    for number, line in enumerate(list_form):
        list_result_single = []
        list_result_single.append(list_form[number][0])
        list_result_single.append(globals()['entry%d' % number].get())  # Получение значения из текстового поля
        list_result.append(list_result_single)
    file = 'result.txt'
    with open(file, 'w') as f:
        f.write(str(list_result))
