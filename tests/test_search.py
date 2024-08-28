'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import pytest
import requests
from models.search import Search
from unittest.mock import patch


@pytest.fixture()
def search():
    return Search()


def test_search_init(search):
    assert True


def test_search_search(search):
    keyword = 'apple'
    with patch('models.search.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'bestMatches': [
                {
                    '1. symbol': 'AAPL',
                    '2. name': 'Apple Inc',
                    '4. region': 'United States',
                }
            ]
        }
        list_of_tuples = search.search(keyword)
        assert list_of_tuples == [('AAPL  (Apple Inc)', 'AAPL')]


def test_search_search_bad_status_code(search):
    with patch('models.search.requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        list = search.search('apple')
        assert list is None


def test_search_search_connection_error(search):
    with patch('models.search.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        list = search.search('apple')
        assert list is None


def test_search_display_sp_100_list(search):
    with patch('models.search.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'bestMatches': [
                {
                    '1. symbol': 'AAPL',
                    '2. name': 'Apple Inc',
                    '4. region': 'United States',
                }
            ]
        }
        list_of_sp_100 = search.display_sp_100_list()
        assert list_of_sp_100 == ['AAPL  (Apple Inc)']
