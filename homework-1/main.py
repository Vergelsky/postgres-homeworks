"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import os
import csv


customers_url = os.path.join('north_data', 'customers_data.csv')
employees_url = os.path.join('north_data', 'employees_data.csv')
orders_data_url = os.path.join('north_data', 'orders_data.csv')

data_urls = [customers_url, employees_url, orders_data_url]


def create_list_from_csv(url_):
    """
    Первым возвращает количество столбцов.
    Вторым возвращает список кортежей значений.
    :url_: путь до csv файла
    :return: Список кортежей элементов строк csv таблицы, кол-во столбцов.
    """
    with open(url_, 'r') as file:
        list_ = [tuple(line) for line in csv.reader(file)]
        return len(list_[0]), list_[1:]


north_conn = psycopg2.connect(host='localhost',
                              database='north',
                              user='postgres',
                              password='5455')


try:
    with north_conn:
        with north_conn.cursor() as cursor:
            #  для каждого адреса
            for url in data_urls:
                #  создаём список атрибутов элементов
                col, data = create_list_from_csv(url)
                #  и записываем его в таблицу с соответствующим названием
                num_of_params = ', '.join(['%s' for n in range(col)])
                for line in data:
                    cursor.execute(f"INSERT INTO {os.path.basename(url)[:-4]} VALUES ({num_of_params})", line)
finally:
    north_conn.close()
