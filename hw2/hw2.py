"""This is hw1 solution.

Напишите модуль, в котором функция process_data принимает путь к json-файлу
с данными о клиентах сайта
(пример файла в data_hw2.json) и путь к json-файлу вывода.
Функция process_data записывает в этот общий json статистику:
процент распределения географии пользователей по городам,
а также процент клиентов, которые были онлайн:
менее двух дней, недели, месяца, полугода, и более полугода назад.
Вынести домашнее и его тесты в отдельную папку hw2.
Тесты используют различные json-файлы.
В workflows выделить отдельные работы для проверок линтера разных домашних,
отдельные работы для тестов разных домашних
(цель состоит в том, чтобы в actions они отображались отдельными галочками).
"""
import json
import os
import os.path as op
from datetime import datetime, timedelta

TWO_DAYS = 2
WEEK = 7
MONTH = 30
HALFYEAR = 180

YEAR_TIME = 2023
MONTH_TIME = 12
DAY_TIME = 18

TIME = datetime(YEAR_TIME, MONTH_TIME, DAY_TIME)


def process_time(dano: dict[str, dict[str, any]]) -> dict:
    """Copmarer of date time for user login and date time of test(per TEST).

    and count latency of time periods for users after rewrite periods to percents

    Args:
        dano (dict[str, dict[str, any]]): consist names of users with their info

    Returns:
        dict: with time result
    """
    two_days_latency = timedelta(days=TWO_DAYS)
    one_week_latency = timedelta(days=WEEK)
    one_month_latency = timedelta(days=MONTH)
    six_monts_latency = timedelta(days=HALFYEAR)
    answer = [0, 0, 0, 0, 0]

    for user in dano.values():
        date_len = TIME - datetime.strptime(user['last_login'], '%Y-%m-%d')
        match date_len:
            case date_len if date_len <= two_days_latency:
                answer[0] += 1
            case date_len if date_len <= one_week_latency:
                answer[1] += 1
            case date_len if date_len <= one_month_latency:
                answer[2] += 1
            case date_len if date_len <= six_monts_latency:
                answer[3] += 1
            case _:
                answer[4] += 1

    for ind, _ in enumerate(answer):
        answer[ind] = answer[ind] / len(list(dano)) * 100

    return {
        'less_than_two_days': answer[0],
        'less_than_week': answer[1],
        'less_than_month': answer[2],
        'less_than_half_year': answer[3],
        'more_than_half_year': answer[4],
    }


def process_cities(dano: dict[str, dict[str, any]]) -> dict:
    """Counter of cities.

    Args:
        dano (dict[str, dict[str, any]]): consist names of users with their info

    Returns:
        dict: with numb of cities
    """
    cities_dano = {}
    for user in dano.values():
        if user['region'] in list(cities_dano):
            cities_dano[user['region']] += 1
        else:
            cities_dano[user['region']] = 1
    return cities_dano


def open_json(file_path: str, output_path: str) -> None:
    """Json file opener.

    Args:
        file_path (str): input file with dicts
        output_path(str): for raise errors

    Returns:
        dano with ifo
    """
    if op.dirname(file_path) and not op.exists(file_path):
        os.makedirs(op.dirname(file_path))
    try:
        with open(file_path, 'r') as filelot:
            dano = json.load(filelot)
    except FileNotFoundError:
        with open(output_path, 'w') as out_file:
            json.dump(
                {'No file was given': None}, fp=out_file,
            )
    except json.JSONDecodeError:
        with open(output_path, 'w') as empty_out_file:
            json.dump(
                {'Given file was empty': None}, fp=empty_out_file,
            )
    return dano


def process_data(source_path: str, dist_path: str) -> None:
    """Solution of hw2.

    Args:
        source_path (str): input file
        dist_path (str): none file if source file were empty
    """
    dano = open_json(source_path, dist_path)
    time_results = process_time(dano)
    cities_results = process_cities(dano)
    with open(dist_path, 'w') as lotfile:
        json.dump(
            {
                'time_results': time_results,
                'cities_results': cities_results,
            },
            fp=lotfile,
            indent=4,
        )
