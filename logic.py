# -*- coding: utf-8 -*-
import re

def request_input():
    with open('database.txt', 'r') as db:
        # Переформатирование базы данных - создание списка списков
        database = []
        for line in db:
            database += [re.split('\t', line)]

        # Удаление символов '\n'
        for i in range(len(database)):
            if database[i][-1][-1] == '\n':
                database[i][-1] = database[i][-1][:-1]

        """
        Пример результата:
        database = [
            ['attr_name', 'display_label', 'value', 'field_type'],
            ['$O.C', 'Цех', '50', 'int'],
            ['$O.U', 'Участок', '123', 'int']
        ]
        """

    while True:  # Цикл, пока ввод не будет корректен

        # Контроль ввода
        try:
            request = input("""
Введите заявки в формате: $Prefix.Name=Value;
Если в качестве Value задать двоеточие, пробел, или оставить пустым,
то в поле фрейм-анкеты значение будет взято из базы данных, иначе будет использовано введенное значение.
Возможен ввод нескольких заявок сразу.
"""
                            )

            form = re.search(r'(\$[A-Za-z]+.[A-Za-z]+=[A-Za-zА-Яа-яЁё0-9 :?.()]*;)+', request)
            # TODO Исправить регулярное выражение - возможен некорректный ввод после первого триплета
            # TODO Подумать над распознаванием ввода триплетов-фактов и триплетов-целей
            request_form = form.group(0)

            # file = 'requests.txt'
            # with open(file, 'w') as f:
            #     f.write(request_form)

            """ Пример запроса:
            $O.C=30;$O.U=11;$O.T=;$O.U=:;$O.C=;$Z.L=12;$O.C=11;$O.U=:;
            """

            request_list1 = re.split(';', request_form)
            request_list1.pop()

            """ Пример результата:
            request_list1 = ['$O.C=50', '$O.U=123']
            """

            request_list = []
            for i in range(len(request_list1)):
                request_list.append(re.split('=', request_list1[i]))

            """ Пример результата:
            request_list = [['$O.C', '50'], ['$O.U', '123']]
            """

            break

        # Контроль формата
        except AttributeError:
            print('Запрос введен в неверном формате. Повторите ввод.')
            continue

        # Control of value
        # except ValueError:
        #    print('\nENTER SOMETHING\n')
        #    #continue

    # Создания списка с данными для заполнения полей фрейм-анкеты
    # global list_form
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
                list_form.append(list_form_single)
    """
    # Пример результата:
    list_form = [
        ['$O.C', 'Цех', '50', 'int'],
        ['$O.U', 'Участок', '123', 'int']
    ]
    """

# Проверка ввода значений в текстовые поля фрейм-анкеты
def input_check():
    # TODO доделать
    for number, line in enumerate(list_form):
        value = globals()['entry%d' % number].get()  # Получение значения из текстового поля
        if list_form[number][3] == 'int':
            int(value)


# Сохранение введенных значений в текстовых полях фрейм-анкеты
def saving_data(list_form):
    # TODO доделать

    list_result = []
    for number, line in enumerate(list_form):
        # print('$prefix.name:', line[0]
        # print('Отображаемое имя:', line[1])
        # print('Значение:', line[2])
        # print('Тип:', line[3])
        list_result_single = []
        list_result_single.append(list_form[number][0])
        list_result_single.append(globals()['entry%d' % number].get())  # Получение значения из текстового поля
        list_result_single.append(list_result)
        file = 'result.txt'
        with open(file, 'w') as f:
            f.write(list_result)
