# -*- coding: utf-8 -*-
import re

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
        request = input('\nEnter your request. Format: $<prefix>.<name>=<value>\n')
        form = re.search(r'(\$[A-Za-z]+.[A-Za-z]+=[A-Za-zА-Яа-яЁё0-9 :?.()]*;)+', request)
        # TODO Исправить регулярное выражение - возможен некорректный ввод после первого триплета
        # TODO Добавить распознавание ввода не только триплетов-фактов, но и триплетов-целей
        request_form = form.group(0)

        # file = 'requests.txt'
        # with open(file, 'w') as f:
        #     f.write(request_form)

        """ Пример запроса:
        # $O.C=50;$O.U=123;
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
list_form = []
for a in range(len(database)):
    for b in range(len(request_list)):
        if request_list[b][0] == database[a][0]:
            list_form_single = []
            list_form_single.append(database[a][0])
            list_form_single.append(database[a][1])
            list_form_single.append(database[a][2])
            list_form_single.append(database[a][3])
            list_form.append(list_form_single)
