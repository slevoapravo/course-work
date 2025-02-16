import json
from datetime import datetime, timedelta

import pandas as pd
from pandas import DataFrame

from src.utils import (currency, greeting, number_cards, path_to_file, read_file, stock_prices, to_file,
                       top_transactions)

begin_date = datetime(2020, 5, 25, 15, 46, 57)
str_begin_date = datetime.strftime(begin_date, "%Y-%m-%d %H:%M:%S")


def get_operations() -> pd.DataFrame:
    """Читаем файл Excel"""
    df = pd.read_excel(path_to_file)

    datetime_fields_to_convert = {
        "Дата операции": "%d.%m.%Y %H:%M:%S",
        "Дата платежа": "%d.%m.%Y",
    }
    for datetime_field, str_format in datetime_fields_to_convert.items():
        df[datetime_field] = pd.to_datetime(df[datetime_field], format=str_format)

    return df


def filter_operations_by_date(df: pd.DataFrame, date: str):
    """Фильтрация транзакций по дате"""
    dt = datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
    start_date = pd.to_datetime(dt.replace(day=1))
    end_date = pd.to_datetime(dt + timedelta(days=1))
    return df.loc[(df["Дата операции"] >= start_date) & (df["Дата операции"] < end_date)]


def main(date):
    data = read_file(filter_operations_by_date(get_operations(), date))

    transactions = ['transactions']

    main_data = {
        "greeting": greeting()["greeting"],
        "cards": number_cards(data),
        "top_transactions": top_transactions(transactions),
        "currency_rates": currency(),
        "stock_prices": stock_prices()
    }

    return main_data



if __name__ == "__main__":
    str_begin_date = "11-11-2021 12:12:12"
    print(main(str_begin_date))