import pytest

from src.services import investment_bank

def test_investment_bank(transactions):
    assert investment_bank("2021-12", transactions, 50) == '[{"investment_bank": 0}]'