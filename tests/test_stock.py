'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import pytest
import requests
from models.stock import Stock
from unittest.mock import patch


@pytest.fixture()
def stock():
    return Stock("AAPL")


def test_stock_init(stock):
    assert stock.symbol == "AAPL"


def test_stock_interval(stock):
    investor_type = "average trader"
    assert stock.interval(investor_type) == "weekly"


def test_stock_fetch_time_series_daily(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Time Series (Daily)': {
                str(i): {'4. close': str(i)}
                for i in range(1, 253)
            }
        }
        dictionary = stock.fetch_time_series("daily")
        assert dictionary == {str(i): i for i in range(1, 253)}


def test_stock_fetch_time_series_weekly(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Weekly Adjusted Time Series': {
                str(i): {'5. adjusted close': str(i)}
                for i in range(1, 500)
            }
        }
        dictionary = stock.fetch_time_series("weekly")
        assert dictionary == {str(i): i for i in range(1, 261)}


def test_stock_fetch_time_series_monthly(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Monthly Adjusted Time Series': {
                str(i): {'5. adjusted close': str(i)}
                for i in range(1, 500)
            }
        }
        dictionary = stock.fetch_time_series("monthly")
        assert dictionary == {str(i): i for i in range(1, 500)}


def test_stock_fetch_time_series_daily_bad_status_code(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        dictionary = stock.fetch_time_series("daily")
        assert dictionary is None


def test_stock_fetch_time_series_weekly_bad_status_code(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        dictionary = stock.fetch_time_series("weekly")
        assert dictionary is None


def test_stock_fetch_time_series_monthly_bad_status_code(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        dictionary = stock.fetch_time_series("monthly")
        assert dictionary is None


def test_stock_fetch_time_series_daily_connection_error(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        dictionary = stock.fetch_time_series("daily")
        assert dictionary is None


def test_stock_fetch_time_series_weekly_connection_error(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        dictionary = stock.fetch_time_series("weekly")
        assert dictionary is None


def test_stock_fetch_time_series_monthly_connection_error(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        dictionary = stock.fetch_time_series("monthly")
        assert dictionary is None


def test_stock_fetch_latest_quote(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Global Quote': {
                '05. price': '100'}
        }
        dictionary = stock.fetch_latest_quote()
        assert dictionary == {'05. price': '100'}


def test_stock_fetch_latest_quote_bad_status_code(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        dictionary = stock.fetch_latest_quote()
        assert dictionary is None


def test_stock_fetch_latest_quote_connection_error(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        dictionary = stock.fetch_latest_quote()
        assert dictionary is None


def test_stock_fetch_company_name(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'Name': 'Apple Inc'}
        name = stock.fetch_company_name()
        assert name == 'Apple Inc'


def test_stock_fetch_company_name_bad_status_code(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        dictionary = stock.fetch_company_name()
        assert dictionary is None


def test_stock_fetch_company_name_connection_error(stock):
    with patch('models.stock.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        dictionary = stock.fetch_company_name()
        assert dictionary is None
