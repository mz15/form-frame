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

    print(database)

file = 'requests.txt'

while True:

    # Control of input
    try:
        request = input('\nEnter your request. Format: $<prefix>.<name>=<value>\n')
        form = re.search(r'\$[A-Za-z]*.[A-Za-z]*=[A-Za-zА-Яа-яЁё0-9 :?.()]*', request)
        request_form = form.group(0)
        with open(file, 'w') as f:
            f.write(request_form)

        request_list = re.split('=', request_form)

        print(request_list)
        break

    # Control of format
    except AttributeError:
        print('Запрос введен в неверном формате. Повторите ввод.')
        continue

    # Control of value
    # except ValueError:
    #    print('\nENTER SOMETHING\n')
    #    #continue
