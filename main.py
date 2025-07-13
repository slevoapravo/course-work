import pandas as pd
import os
from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import get_xlsx_data_dict
from src.views import main_page

if __name__ == "__main__":
    result_main_page = main_page("2021-12-31 23:59:59")

    transactions = get_xlsx_data_dict('data/operations.xlsx')
    result_services = investment_bank("2021-12", transactions, 50)

    transcations_df = pd.read_excel("data/operations.xlsx")
    result_reports = spending_by_category(
        transcations_df, "Каршеринг", "2021-12-31 15:45:34"
    )

    print(result_main_page)
    print(result_services)
    print(result_reports)