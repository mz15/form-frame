# -*- coding: utf-8 -*-
import sys
import re
from vsptd import parse_trp_str


def get_args():
    """ПОЛУЧИТЬ ПАРАМЕТРЫ ИЗ КОМАНДНОЙ СТРОКИ
    Парсинг реквизитов из первого параметра, разбор триплетной строки из второго
    Возвращает:
        list(list, TrpStr) - (реквизиты, триплетная строка)
    """
    # реквизит
    RE_REQST = re.compile(r"\$([A-Za-z]+\d*)\.([A-Za-z]+)(?:(\||:)('?[A-Za-zА-Яа-яЁё0-9 :.?()]*'?)?)?")

    args = sys.argv[1:]  # получение аргументов из командной строки
    if len(args) == 0:
        raise ValueError('Не принято ни одного аргумента')

    requisites = re.findall(RE_REQST, args[0])  # реквизиты
    if len(requisites) == 0:
        raise ValueError('Неверный формат реквизитов')

    addnl_pars = ''  # дополнительные параметры
    try:
        addnl_pars = parse_trp_str(args[1])
    except IndexError:
        pass

    return requisites, addnl_pars

if __name__ == '__main__':
    # тестирование
    from pprint import pprint
    pprint(get_args())
