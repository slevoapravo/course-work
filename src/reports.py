import datetime
import json
import logging
from datetime import timedelta
from typing import Any, Callable
import pandas as pd


logger = logging.getLogger("report.log")
file_handler = logging.FileHandler("report.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def decorator_spending_by_cat(func: Callable) -> Callable:
    """Логирует результат функции в файл по умолчанию spending_by_cat.json"""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs).to_dict("records")
        with open("spending_by_cat.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result

    return wrapper


def log_spending_by_cat(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict("records")
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result
        return wrapper
    return decorator


def filtering_by_date(operations_df: pd.DataFrame, date: str) -> pd.DataFrame:
    """Возвращает DataFrame за 3 месяца от указанной даты"""
    logger.info("Converting DF to dictionary")
    operations = operations_df.to_dict("records")
    filtered_operations = []
    logger.info("Creating period for 90 days")
    current_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    end_date = current_date - timedelta(days=90)
    logger.info("Filtering operations within 3 months period")
    for operation in operations:
        payment_date = datetime.datetime.strptime(
            str(operation["Дата операции"]), "%d.%m.%Y %H:%M:%S"
        )
        if end_date < payment_date < current_date:
            filtered_operations.append(operation)
    logger.info("Converting data back to DF")
    filtered_operations_df = pd.DataFrame(filtered_operations)
    logger.info("Returning DF to main function")
    return filtered_operations_df


@decorator_spending_by_cat
def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> pd.DataFrame:
    """Возвращает DataFrame по заданной категории за 3 месяца от указанной даты"""
    logger.info("Start")
    logger.info(
        "Creating filtered list by date for last 3 months with another function"
    )
    transactions_filtered_by_3_months = filtering_by_date(transactions, date)
    logger.info("Filtering transactions by category")
    if transactions_filtered_by_3_months.empty:
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если нет транзакций
    category_transcations = transactions_filtered_by_3_months[
        transactions_filtered_by_3_months["Категория"] == category]
    logger.info("Returning filtered DF")
    logger.info("Stop")
    return category_transcations

