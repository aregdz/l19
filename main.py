#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import jsonschema

def help1():
    """"
    Функция для вывода списка команд
    """
    # Вывести справку о работе с программой.
    print("Список команд:\n")
    print("add - добавить рейс;")
    print("list - вывести список рйсов;")
    print("select <тип> - вывод на экран пунктов назначения и номеров рейсов для данного типа самолёта")
    print("select <стаж> - запросить работников со стажем;")
    print("help - отобразить справку;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("exit - завершить работу с программой.")


def add1():
    """"
    Функция для добавления информации о новых рейсах
    """
    # Запросить данные о работнике.
    name = input("Название пункта назначения рейса? ")
    number = int(input("Номер рейса? "))
    tip = input("Тип самолета? ")
    # Создать словарь.
    i = {
        'name': name,
        'number': number,
        'tip': tip,
    }

    return i


def error1(command):
    """"
    функция для неопознанных команд
    """
    print(f"Неизвестная команда {command}")


def list(aircrafts):
    """"
    Функция для вывода списка добавленных рейсов
    """
    # Заголовок таблицы.
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 8
    )
    print(line)

    # Вывести данные о всех сотрудниках.
    for idx, i in enumerate(aircrafts, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                idx,
                i.get('name', ''),
                i.get('number', ''),
                i.get('tip', '')
            )
        )
    print(line)


def validate_json_data(data):

    schema = {
    "title": "Aircrafts",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "number": {"type": "integer"},
            "tip": {"type": "string"}
        },
        "additionalProperties": False,
        "required": ["name", "number", "tip"]
    }
}

    try:
        jsonschema.validate(data, schema)
        print("Данные прошли валидацию.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print("Ошибка валидации данных:", e)
        return False

def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кириллицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        n = json.load(fin)
        if validate_json_data(n):
            return n
        else:
            return False

def select(command, aircrafts):
    """""
    Функция для получения номера рейса и пункта назначения по заднному типу самолёта.
    """
    # Разбить команду на части для выделения номера года.
    parts = command.split(' ', maxsplit=1)
    # Проверить сведения работников из списка.
    count = 0

    for i in aircrafts:
        for k, v in i.items():

            if v == parts[1]:
                print("Пункт назначения - ", i["name"])
                print("Номер рейса - ", i["number"])
                count += 1
    # Если счетчик равен 0, то работники не найдены.

    if count == 0:
        print("Рейс с заданным типом самолёта не найден.")


def main1():
    """"
    Главная функция программы.
    """
    print("Список команд:\n")
    print("add - добавить рейс;")
    print("list - вывести список рйсов;")
    print("select <тип> - вывод на экран пунктов назначения и номеров рейсов для данного типа самолёта")
    print("select <стаж> - запросить работников со стажем;")
    print("help - отобразить справку;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("exit - завершить работу с программой.")
    # Список работников.
    aircrafts = []
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()
        # Выполнить действие в соответствие с командой.

        if command == 'exit':
            break

        elif command == 'add':
            # Добавить словарь в список.
            i = add1()
            aircrafts.append(i)
            # Отсортировать список в случае необходимости.
            if len(aircrafts) > 1:
                aircrafts.sort(key=lambda item: item.get('name', ''))

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_workers(file_name, aircrafts)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            aircrafts = load_workers(file_name)

        elif command == 'list':
            list(aircrafts)

        elif command.startswith('select '):
            select(command, aircrafts)

        elif command == 'help':
            help1()

        else:
            error1("command")


if __name__ == '__main__':
    main1()
