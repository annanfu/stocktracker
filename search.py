'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import requests
import streamlit as st

APIKEY = 'DFYILHJL9BDQIV0S'

# A constant of list of 100 SP stocks
SP100 = [
    'AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'AIG', 'AMD', 'AMGN', 'AMT', 'AMZN',
    'AVGO', 'AXP', 'BA', 'BAC', 'BK', 'BKNG', 'BLK', 'BMY', 'C', 'CAT',
    'CHTR', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CRM', 'CSCO', 'CVS', 'CVX',
    'DE', 'DHR', 'DIS', 'DOW', 'DUK', 'EMR', 'EXC', 'F', 'FDX', 'GD', 'GE',
    'GILD', 'GM', 'GOOG', 'GOOGL', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM',
    'KHC', 'KO', 'LIN', 'LLY', 'LMT', 'LOW', 'MA', 'MCD', 'MDLZ', 'MDT', 'MET',
    'META', 'MMM', 'MO', 'MRK', 'MS', 'MSFT', 'NEE', 'NFLX', 'NKE', 'NVDA', 'ORCL',
    'PEP', 'PFE', 'PG', 'PM', 'PYPL', 'QCOM', 'RTX', 'SBUX', 'SCHW', 'SO', 'SPG',
    'T', 'TGT', 'TMO', 'TMUS', 'TSLA', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VZ',
    'WFC', 'WMT', 'XOM'
]


class Search():
    '''
    A search is a funtionality to look for the result.
    '''
    def __init__(self):
        '''
        This method is the constructor of the search objects.
        Parameters: None
        Return: None
        '''
        pass

    def search(self, keyword):
        """
        This method fetches a the best-matching symbols based on keywords.
        parameters: keyword -- string, user input keyword
        return: dictionary, best matches of symbols
        """
        # Fetch the best-matching symbols based on keywords
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={APIKEY}"
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.ConnectionError:
            return
        if response.status_code != 200:
            return

        # Iterate through the data and put the stocks that are in US market in list
        list_of_dict_matches = data["bestMatches"]
        list_of_tuples = []
        for matches in list_of_dict_matches:
            if matches["4. region"] == "United States":
                tuple = (matches["1. symbol"] + "  (" + matches["2. name"] + ")", matches["1. symbol"])
                list_of_tuples.append(tuple)
        return list_of_tuples

    @st.cache_data
    def display_sp_100_list(_self):
        """
        This method creates the sp100 index component stock list.
        parameters: None
        return: list, company discriptions
        """
        list = SP100
        list_of_sp_100 = []
        # iterate through the best-match list and put the company names in list
        for symbol in list:
            tuple = _self.search(symbol)[0]
            if tuple[1] == symbol:
                list_of_sp_100.append(tuple[0])
        return list_of_sp_100
