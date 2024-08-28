'''
Annan Fu
CS 5001, Fall 2023
Final Project -- analysis tracker
This application is a analysis tracker with tailored features
based on investor type.
'''
import pytest
import requests
from models.analysis import Analysis
from unittest.mock import patch


@pytest.fixture()
def analysis():
    return Analysis("AAPL")


def test_analysis_init(analysis):
    assert analysis.symbol == "AAPL"


def test_analysis_fetch_news(analysis):
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'feed': ["new_1", "news_2"]
        }
        list = analysis.fetch_news()
        assert list == ["new_1", "news_2"]


def test_analysis_fetch_news_bad_status_code(analysis):
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        list = analysis.fetch_news()
        assert list is None


def test_analysis_news_technical_analysis(analysis):
    list_news_feed = [
        {
            "ticker_sentiment": [
                {"ticker": "AAPL",
                 "ticker_sentiment_label": "Somewhat-Bullish"},
                {"ticker": "AAPL",
                 "ticker_sentiment_label": "Bearish"}
            ]
        }
    ]
    bearish_count, bullish_count = analysis.news_technical_analysis(list_news_feed)
    assert bullish_count == 1
    assert bearish_count == 1


def test_analysis_rsi_analysis(analysis):
    interval = 'daily'
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Meta Data': {
                '3: Last Refreshed': '2023-11-27'
            },
            'Technical Analysis: RSI': {
                '2023-11-27': {
                    'RSI': '50'
                    }
            }
        }
        rsi_value = analysis.rsi_analysis(interval)
        assert rsi_value == '50'


def test_analysis_rsi_analysis_bad_status_code(analysis):
    interval = "daily"
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        rsi_value = analysis.rsi_analysis(interval)
        assert rsi_value is None


def test_analysis_sma_analysis(analysis):
    interval = 'monthly'
    period = 60
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Meta Data': {
                '3: Last Refreshed': '2023-11-27'
            },
            'Technical Analysis: SMA': {
                '2023-11-27': {
                    'SMA': '100'
                    }
            }
        }
        sma_value = analysis.sma_analysis(interval, period)
        assert sma_value == '100'


def test_analysis_company_overview(analysis):
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'LatestQuarter': '2023-09-30',
            'EPS': '20'
        }
        dict_overview, cut_off_date = analysis.company_overview()
        assert dict_overview == {
            'LatestQuarter': '2023-09-30',
            'EPS': '20'
        }
        assert cut_off_date == '2023-09-30'


def test_analysis_sma_analysis_bad_status_code(analysis):
    interval = "weekly"
    period = 10
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        sma_value = analysis.sma_analysis(interval, period)
        assert sma_value is None


def test_analysis_company_overview_bad_status_code(analysis):
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        value = analysis.company_overview()
        assert value is None


def test_analysis_fetch_news_connection_error(analysis):
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        list = analysis.fetch_news()
        assert list is None


def test_analysis_rsi_analysis_connection_error(analysis):
    interval = "daily"
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        rsi_value = analysis.rsi_analysis(interval)
        assert rsi_value is None


def test_analysis_sma_analysis_connection_error(analysis):
    interval = "daily"
    period = 60
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        sma_value = analysis.sma_analysis(interval, period)
        assert sma_value is None


def test_analysis_company_overview_connection_error(analysis):
    with patch('models.analysis.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        overview_value = analysis.company_overview()
        assert overview_value is None
