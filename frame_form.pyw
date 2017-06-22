# -*- coding: utf-8 -*-
from tkinter import Tk, Frame, Label, Entry, Button, filedialog, Toplevel
from tkinter.messagebox import *
# from lxml import etree  # Библиотека импортируется в конце кода в блоке try


def error_massage_box():
    if error_code == 'file_not_selected':
        msg_title = 'Ошибка. Файл не выбран'
        msg_text = 'Вы не выбрали XML-файл, на основе которого будет сгенерирована фрейм-анкета.'

    if error_code == 'file_not_found':
        msg_title = 'Ошибка. Файл не найден'
        msg_text = 'Выбранный XML-файл не найден. Возможно, он был удален или переименован. ' \
                   'Необходимо повторить выбор файла'

    if error_code == 'invalid_format':
        msg_title = 'Ошибка. Неверный формат'
        msg_text = 'Данные не сохранены. ' \
                   'Одно или несколько значений не соответствуют требуемому формату.'

    showerror(msg_title, msg_text)

def info_massage_box():
    if info_code == 'successful_file_saving':
        msg_title = 'Данные сохранены'
        msg_text = 'Данные успешно записаны в файл ' + str(res_file)

    showinfo(msg_title, msg_text)


def choose_file(event):  # Выбор XML-файла
    global xml_file

    file_types = [('XML files', '.xml')]  # Файловый фильтр
    xml_file = filedialog.askopenfilename(title='Выберите XML-файл', filetypes=file_types)  # Путь к выбранному файлу

    if len(xml_file) != 0:
        lbl1 = Label(fields_frame, fg='green', text=xml_file)  # display_label
        lbl1.grid(row=1, column=0, padx=20, pady=5)
    else:
        lbl1 = Label(fields_frame, fg='red', text='Файл не выбран')  # display_label
        lbl1.grid(row=1, column=0, padx=20, pady=5)


def create_list_form():  # Чтение и преобразование данных для генерации фрейм-анкеты
    with open(xml_file, 'rb') as fobj:
#    with open(xml_file, encoding='utf-8') as fobj:
        xml = fobj.read()

    list_form = []  # Список с данными для заполнения полей фрейм-анкеты
    global caption_table, root
    root = etree.fromstring(xml)

    for DATAPACKET in root.getchildren():  # METADATA, ROWDATA
        for DATA in DATAPACKET.getchildren():  # FIELDS, PARAMS, ROW
            if DATA.tag == 'FIELDS':
                pass
            if DATA.tag == 'PARAMS':
                attr_params = DATA.attrib  # Атрибуты тега ROW

                caption_table = attr_params.get('CAPTION_TABLE', 'Заголовок не задан')  # Заголовок XML-таблицы
            if DATA.tag == 'ROW':
                attr_row = DATA.attrib  # Атрибуты тега ROW
                list_form.append(attr_row.values())  # Добавление списка занчений атрибутов ROW в общий список

    return list_form

def check_values(event):
    list_form = create_list_form()
    list_result = []  # Список с данными, введенными пользователем в текстовые поля
    discrepancy = []  # Список с кодами наличия ошибки формата: 1 - есть ошибка, 0 - нет ошибки

    for number, line in enumerate(list_form):
        value = globals()['entry%d' % number].get()  # Получение значения текстового поля
        list_result.append(value)
        field_format = globals()['prompt%d' % number]["text"]  # Получение формата

        if len(value) > 0:
            if field_format.startswith('X('):  # Если формат вида X(10) - текст из 10 любых символов
                field_format = field_format[2:-1]  # Преобразуем в целое число
                if len(value) > int(field_format):  # Если кол-во символов в значении больше чем должно быть
                    discrepancy.append('1')
                else:
                    discrepancy.append('0')

            elif field_format.isalpha():  # Если формат вида XXXX - текст из 4 любых символов
                if len(value) > len(field_format):  # Если кол-во символов в значении больше чем, в формате
                    discrepancy.append('1')
                else:
                    discrepancy.append('0')

            elif field_format.isdigit():  # Если формат виде 9999 - четырехзначное целое число
                if len(value) <= len(field_format) and value.isdigit():  # Если значение соответствует формату
                    discrepancy.append('0')
                else:
                    discrepancy.append('1')

            elif field_format.startswith('9('):  # Если формат виде 9(3) - трехзначное целое число
                field_format = field_format[2:-1]  # Преобразуем в целое число
                try:
                    int(value)
                    if len(value) > int(field_format):  # Если кол-во символов в значении больше чем должно быть
                        discrepancy.append('1')
                    else:
                        discrepancy.append('0')
                except ValueError:  # Если значение не является целым числом
                    discrepancy.append('1')

            elif field_format.find('V') > 0:  # Если формат вида 999V999 или S999V999 - +/- действительное число
                try:
                    if field_format.find('S') == -1:  # Если формат вида 999V999 - положительное действительное число
                        if float(value) < 0:  # Если значение - отрицательное действительное число
                            discrepancy.append('1')
                        elif float(value) == 0:  # Если значение - 0
                            discrepancy.append('0')
                        else:  # Если значение - положительное действительное число
                            ff0 = field_format.split('V')[0]  # Целая часть числа в формате
                            ff1 = field_format.split('V')[1]  # Дробная часть числа в формате
                            if value.find('.') == -1:  # Если введена только целая часть числа
                                if len(value) <= len(ff0):  # Если длины целых частей равны
                                    discrepancy.append('0')
                                else:
                                    discrepancy.append('1')
                            else:  # Если введена целая часть числа и дробная
                                v0 = value.split('.')[0]  # Целая часть числа в значении
                                v1 = value.split('.')[1]  # Дробная часть числа в значении

                                if len(v0) <= len(ff0) and len(v1) <= len(ff1): # Если длины частей не превышают формат
                                    discrepancy.append('0')
                                else:
                                    discrepancy.append('1')
                    elif field_format.find('S') == 0:  # Если формат вида S999V999 - отрицательное действительное число
                        if float(value) < 0:  # Если значение - отрицательное действительное число
                            ff0 = field_format.split('V')[0]  # Целая часть числа в формате
                            ff1 = field_format.split('V')[1]  # Дробная часть числа в формате
                            if value.find('.') == -1:  # Если введена только целая часть числа
                                if len(value) <= len(ff0):  # Если длины целых частей равны
                                    discrepancy.append('0')
                                else:
                                    discrepancy.append('1')
                            else:  # Если введена целая часть числа и дробная
                                v0 = value.split('.')[0]  # Целая часть числа в значении
                                v1 = value.split('.')[1]  # Дробная часть числа в значении

                                if len(v0) <= len(ff0) and len(v1) <= len(ff1): # Если длины частей не превышают формат
                                    discrepancy.append('0')
                                else:
                                    discrepancy.append('1')
                        else:
                            discrepancy.append('1')

                except ValueError:  # Если значение не является действительным числом
                    discrepancy.append('1')

    if discrepancy.count('1') > 0:  # Если есть хотя бы одно значение с неверным форматом
        global error_code
        error_code = 'invalid_format'
        error_massage_box()
    else:
        save_xml()



#    for element in discrepancy:
#        if element == 0:
#            continue
#        else:




def save_xml():
    list_form = create_list_form()
    list_result = []  # Список с данными, введенными пользователем в текстовые поля
#    list_check = []

    for number, line in enumerate(list_form):
        list_result.append(globals()['entry%d' % number].get())  # Получение значения из текстового поля
#        list_check.append(globals()['prompt%d' % number]["text"])  # Получение формата
#    print(list_check)
    i = 0  # Номер элемента списка list_result
    for DATAPACKET in root.getchildren():  # METADATA, ROWDATA
        for DATA in DATAPACKET.getchildren():  # FIELDS, PARAMS, ROW
            if DATA.tag == 'ROW':
                DATA.attrib['Q.K'] = list_result[i]  # Замена исходного значения на введенное пользователем
                i += 1  # Переход к следующей элементу списка list_result (следующая строка)

    global info_code, error_code, res_file
    res_title = 'Введите имя нового файла или выберите существующий для замены'
    res_file_types = [('XML files', '.xml')]  # Файловый фильтр
    res_f_name_default = 'result_xml_file.xml'
    # Путь к выбранному файлу
    res_file = filedialog.asksaveasfilename(title=res_title,  # Заголовок диалогового окна
                                            filetypes=res_file_types,  # Файловый фильтр
                                            initialfile=res_f_name_default)  # Имя файла по умолчанию

    if len(res_file) > 0:
        if res_file.endswith('.xml') is False:  # Если неверное расширение файла
            res_file = str(res_file) + '.xml'
    
    try:
        with open(res_file, 'wb') as out:
            out.write(etree.tostring(root, pretty_print=False, xml_declaration=False))

        info_code = 'successful_file_saving'
        info_massage_box()

    except FileNotFoundError:
        pass

def check(event):  # Функция проверки наличия выбранного XML-файла
    global error_code
    try:  # Если файл выбран и найден
        frame_window(event)

    except FileNotFoundError:  # Если файл не найден (не выбран, удален и т.д.)
        if len(xml_file) == 0:
            error_code = 'file_not_selected'
        if len(xml_file) > 0:
            error_code = 'file_not_found'
        error_massage_box()

    except NameError:  # Если файл не выбран (ниразу не была нажата кнопка выбора)
        error_code = 'file_not_selected'
        error_massage_box()

def frame_window(event):
    list_form = create_list_form()

    frame_window = Toplevel()
    frame_window.grab_set()
    frame_window.focus_set()
    frame_window.title("Фрейм-анкета — " + caption_table)
    frame_window.maxsize(width=1300, height=636)

    btn_frame = Frame(frame_window)
    btn_frame.pack()

    fields_frame = Frame(frame_window)
    fields_frame.pack()

    btn = Button(btn_frame,
                 text="Сохранить",  # Надпись на кнопке
                 width=20  # Ширина
                 # height=3,  # Высота
                 # bg = "grey",
                 # fg = "blue"  # Цвет фона и надписи
                 )
    btn.grid(row=0, column=0, padx=0, pady=10)
    btn.bind("<ButtonRelease-1>", check_values)  # Вызов функции по нажатию на кнопку

    # Создание полей
    for number, line in enumerate(list_form):
        globals()['label%d' % number] = Label(fields_frame, text=line[3])  # display_label
        globals()['label%d' % number].grid(row=number, column=0, padx=20, pady=5)

        globals()['entry%d' % number] = Entry(fields_frame, width=50, bd=2)  # value
        globals()['entry%d' % number].grid(row=number, column=1, padx=0, pady=5)
        globals()['entry%d' % number].insert(0, line[4])  # Значение по умолчанию (введенное или из базы данных)

        globals()['prompt%d' % number] = Label(fields_frame, text=line[2])  # display_label
        globals()['prompt%d' % number].grid(row=number, column=2, padx=10, pady=5)


root = Tk()
root.title("Генератор фрейм-анкеты")
# root.minsize(width=700, height=400)

# Контейнеры для кнопок и полей
btn_frame = Frame(root)
btn_frame.pack()

fields_frame = Frame(root)
fields_frame.pack()

# Создание кнопок
btn_select = Button(btn_frame,
             text='Выбрать файл — словарь метаданных',  # Надпись на кнопке
             width=35  # Ширина
             # height=3,  # Высота
             # bg = "grey",
             # fg = "blue"  # Цвет фона и надписи
             )

btn_generate = Button(btn_frame,
             text='Сгенерировать фрейм-анкету',  # Надпись на кнопке
             width=35  # Ширина
             # height=3,  # Высота
             # bg = "grey",
             # fg = "blue"  # Цвет фона и надписи
             )


btn_select.grid(row=0, column=0, padx=10, pady=10)
btn_select.bind("<ButtonRelease-1>", choose_file)  # Вызов функции по нажатию на кнопку

btn_generate.grid(row=0, column=1, padx=10, pady=10)
btn_generate.bind("<ButtonRelease-1>", check)  # Вызов функции по нажатию на кнопку frame_window

# Создание полей
lbl_text = 'Выберите файл — словарь метаданных в формате XML, на основе которого будет сгенерирована фрейм-анкета'
lbl = Label(fields_frame, text=lbl_text)  # display_label
lbl.grid(row=0, column=0, padx=20, pady=5)

try:
    from lxml import etree
except ImportError:
    showerror('Ошибка', 'Внимание! На данном компьютере не установлена библиотека lxml для обработки XML-файлов. '
                        'Без нее программа не будет корректно работать и не сможет сгенерировать фрейм-анкету. '
                        'Необходимо установить библиотеку и повторно запустить программу.')

root.mainloop()

