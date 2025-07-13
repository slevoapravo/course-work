import datetime
import json
import logging
from typing import Any, Dict, List

from src.utils import get_xlsx_data_dict

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("services.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """Рассчитывает сумму на счету инвесткопилки по заданному порогу округления"""
    logger.info("Start")
    period = datetime.datetime.strptime(month, "%Y-%m")
    logger.info("Creating filtered transactions list")
    transactions_list = []
    investment_bank_sum = 0
    logger.info(
        "Filtering transactions by date and putting their sum into filtered transactions list"
    )
    for transaction in transactions:
        transaction_date = transaction["operation_date"]
        payment_date = datetime.datetime.strptime(transaction_date, "%d.%m.%Y %H:%M:%S")
        if payment_date.month == period.month and transaction["payment_sum"] < 0:
            transactions_list.append(transaction["payment_sum"])
    logger.info("Calculating remaining sum for investment bank")
    for transact in transactions_list:
        sum = abs(transact)
        diff = (sum // limit + 1) * limit - sum
        investment_bank_sum += diff
    logger.info("Creating json-file with sum for investment bank")
    result_list = []
    result_dict = {}
    result_dict["investment_bank"] = round(investment_bank_sum, 2)
    result_list.append(result_dict)
    result_list_jsons = json.dumps(result_list)
    logger.info("Stop")
    return result_list_jsons

