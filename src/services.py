import json
import logging
from datetime import datetime
from logging import FileHandler
from pathlib import Path
from typing import Any, Dict, List
import openpyxl

# Настройка логгирования
logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
path_to_project = Path(__file__).resolve().parent.parent
path_to_file = path_to_project / "data" / "operations.xlsx"
fileHandler = FileHandler(path_to_project / "logs" / "services.log", encoding="UTF-8", mode="w")
fileFormatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fileHandler.setFormatter(fileFormatter)
logger.addHandler(fileHandler)

# Указание даты
date_obj = datetime(2021, 5, 31)
str_date_service = datetime.strftime(date_obj, "%Y-%m")

# Загрузка данных из Excel
def load_transactions(file_path: Path) -> List[Dict[str, Any]]:
    transactions = []
    try:
        logger.info("Загрузка данных из файла...")
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = dict(zip(headers, row))
            transactions.append({
                "Дата операции": row_data["Дата операции"],
                "Дата платежа": row_data["Дата платежа"],
                "Номер карты": row_data["Номер карты"],
                "Статус": row_data["Статус"],
                "Сумма операции": row_data["Сумма операции"],
                "Валюта операции": row_data["Валюта операции"],
                "Сумма платежа": row_data["Сумма платежа"],
                "Валюта платежа": row_data["Валюта платежа"],
                "Кэшбэк": row_data["Кэшбэк"],
                "Категория": row_data["Категория"],
                "MCC": row_data["MCC"],
                "Описание": row_data["Описание"],
                "Бонусы (включая кэшбэк)": row_data["Бонусы (включая кэшбэк)"],
                "Округление на инвесткопилку": row_data["Округление на инвесткопилку"],
                "Сумма операции с округлением": row_data["Сумма операции с округлением"],
            })
            if len(transactions) == 1500:
                logger.info("Загружено 1500 транзакций, дальнейшая загрузка прекращена.")
                break
        logger.info("Данные успешно загружены.")
    except Exception as e:
        logger.exception("Ошибка при загрузке транзакций.")
    return transactions

# Функция для вычисления экономии
def investment_bank(month: str, list_transactions: List[Dict[str, Any]], limit: int) -> str:
    """Подсчет округленных транзакций за данный месяц."""
    try:
        logger.info("Начало подсчета экономии...")
        counter = 0
        for transaction in list_transactions:
            payment_date_str = transaction.get("Дата платежа")
            if payment_date_str:
                payment_date = datetime.strptime(payment_date_str, "%d.%m.%Y")
                if payment_date.strftime("%Y-%m") == month:
                    payment = transaction.get("Сумма платежа", 0)
                    if payment < 0:  # Если сумма платежа отрицательная
                        investment = round(int(payment) // limit) * limit
                        counter += investment
        logger.info(f"Сумма экономии составляет: {counter}")
        return json.dumps(float(str(counter)[1:]), ensure_ascii=False) if counter else "0"
    except Exception as e:
        logger.exception("Ошибка в процессе подсчета экономии.")
        return "0"

if __name__ == "__main__":
    transactions = load_transactions(path_to_file)
    print(investment_bank(str_date_service, transactions, 50))
