import datetime
import json
import os
from typing import Any, Dict, List

import pandas as pd
import requests
import result
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()

api_key = os.getenv("API_KEY")


def get_xlsx_data_dict(file_name: str) -> List[Dict]:
    """Считывает данные о финансовых операциях из excel файла и преобразует их в список словарей"""
    try:
        xlsx_data = pd.read_excel(file_name)
        data_list = xlsx_data.apply(
            lambda row: {
                "operation_date": row["Дата операции"],
                "payment_date": row["Дата платежа"],
                "card_number": row["Номер карты"],
                "status": row["Статус"],
                "operation_sum": row["Сумма операции"],
                "operation_cur": row["Валюта операции"],
                "payment_sum": row["Сумма платежа"],
                "payment_cur": row["Валюта платежа"],
                "cashback": row["Кэшбэк"],
                "category": row["Категория"],
                "MCC": row["MCC"],
                "description": row["Описание"],
                "Bonus": row["Бонусы (включая кэшбэк)"],
                "Invest_bank": row["Округление на инвесткопилку"],
                "rounded_operation_sum": row["Сумма операции с округлением"],
            },
            axis=1,
        )
        new_dict_list = []
        row_index = 0
        for row in data_list:
            new_dict_list.append(data_list[row_index])
            row_index += 1
        return new_dict_list

    except Exception:
        return "File can't be read"


def get_greeting(time_data: str) -> str:
    """Принимает текущее время и возвращает приветствие в зависимости от времени суток"""
    if 0 <= int(time_data[11:13]) <= 5:
        return "Доброй ночи"
    elif 6 <= int(time_data[11:13]) <= 11:
        return "Доброе утро"
    elif 12 <= int(time_data[11:13]) <= 17:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_time_data() -> str:
    """Возвращает текущее время"""
    time_data = datetime.datetime.now()
    return str(time_data)


time_data = get_time_data()
greeting = get_greeting(time_data)
print(time_data)


def get_card_number_list(transactions: List[Dict[Any, Any]]) -> list:
    """Выводит список уникальных номеров карт из списка транзакций"""
    card_list_full = []
    for transaction in transactions:
        if transaction["card_number"]:
            card_list_full.append(transaction["card_number"])
    card_list_short = []
    for card in card_list_full:
        if card not in card_list_short and type(card) is str:
            card_list_short.append(card)
    return card_list_short


def get_operations_sum(
        time_data: str, transactions: List[Dict[str, Any]], card_number: str
) -> float:
    """Выводит общую сумму расходов по номеру карты в формате *1234"""
    month = time_data[5:7] + "." + time_data[:4]
    transactions_sum_list = []
    for transaction in transactions:
        date = str(transaction["payment_date"])
        if (
                transaction["card_number"] == card_number
                and date[3:] == month
                and transaction["payment_sum"] < 0
        ):
            transactions_sum_list.append(transaction["payment_sum"])
    total_operations_sum = abs(sum(transactions_sum_list))
    return total_operations_sum


transactions = get_xlsx_data_dict('../data/operations.xlsx')
card_number_list = get_card_number_list(transactions)
december_date = "2021-12-03"
card_4556 = get_operations_sum(december_date, transactions, "*4556")


def get_cashback_sum(operations_sum: float) -> float:
    """Высчитывает процент кэшбэка от общей суммы(1%)"""
    cash_back_sum = round(operations_sum / 100, 2)
    return cash_back_sum


transactions = get_xlsx_data_dict('../data/operations.xlsx')
december_date = "2021-12-03"
operations_sum_result = get_operations_sum(december_date, transactions, "*7197")
print(type(result))


def show_cards(time_data: str, transactions: List[Dict[Any, Any]]) -> List[Dict]:
    """Выводит информацию по каждой карте (последние 4 цифры карты, общая сумма расходов, кэшбэк)"""
    show_cards_list = []
    cards_list = get_card_number_list(transactions)
    for card in cards_list:
        total_spent = get_operations_sum(time_data, transactions, card)
        card_dict = {}
        card_dict["last_digits"] = card[1:]
        card_dict["total_spent"] = get_operations_sum(time_data, transactions, card)
        card_dict["cashback"] = get_cashback_sum(total_spent)
        show_cards_list.append(card_dict)
    return show_cards_list


result = show_cards(december_date, transactions)
print(result)


def show_top_5_transactions(
        time_data: str, transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Выводит информацию о 5 топ транзакциях по сумме платежа"""
    for transaction in transactions:
        neg_sum = transaction["payment_sum"]
        transaction["payment_sum"] = abs(neg_sum)
    month = time_data[5:7] + "." + time_data[:4]
    month_transactions = []
    for transaction in transactions:
        date = str(transaction["payment_date"])
        if date[3:] == month:
            month_transactions.append(transaction)
    sorted_transactions = sorted(
        month_transactions,
        key=lambda transaction: transaction["payment_sum"],
        reverse=True,
    )
    list_index = 1
    top_5_transactions = []
    for transaction in sorted_transactions:
        if list_index < 6:
            top_transaction_dict = {}
            top_transaction_dict["date"] = transaction["payment_date"]
            top_transaction_dict["amount"] = transaction["payment_sum"]
            top_transaction_dict["category"] = transaction["category"]
            top_transaction_dict["description"] = transaction["description"]
            top_5_transactions.append(top_transaction_dict)
            list_index += 1
    return top_5_transactions




def fetch_and_show_currency_rates() -> List[Dict[str, Any]]:
    """Выводит курс валют и записывает из в файл .json"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        payload = {}
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        print(response)
        result = response.json()
        print(result)
        exchange_rates_list = []
        usd_rate = {"currency": "USD", "rate": round(result['Valute']['USD']['Value'], 2)}
        eur_rate = {"currency": "EUR", "rate": round(result['Valute']['EUR']['Value'], 2)}
        exchange_rates_list.append(usd_rate)
        exchange_rates_list.append(eur_rate)
        with open("user_settings.json", "w") as f:
            json.dump(exchange_rates_list, f)
        return exchange_rates_list
    except RequestException:
        return [{}]


exchange_rates = fetch_and_show_currency_rates()
print(exchange_rates)


def fetch_and_show_stock_prices() -> List[Dict[str, Any]]:
    pass