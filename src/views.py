import json
from datetime import datetime, timedelta

import pandas as pd

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
    # Чтение файла с данными
    data = read_file(date)  # Убедитесь, что read_file возвращает правильный объект

    main_data = {
        "greeting": greeting(),
        "cards": number_cards(data, greeting()),
        "top_transactions": top_transactions(data),
        "currency_rates": currency(data),
        "stock_prices": stock_prices(data)
    }

    return json.dumps(main_data, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    str_begin_date = "2023-01-01"
    print(main(str_begin_date))