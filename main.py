from src.reports import df_file, spending_by_weekday, str_date_report
from src.services import investment_bank, str_date_service, transactions
from src.utils import currency, greeting, number_cards, read_file, stock_prices, to_file, top_transactions
from src.views import main, str_begin_date



if __name__ == "__main__":
    str_begin_date = "2023-01-01"
    print(main(str_begin_date))
