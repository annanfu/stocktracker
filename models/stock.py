'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import requests

APIKEY = 'DFYILHJL9BDQIV0S'
TRADE_DAYS_PER_YEAR = 252   # 252 trading days in the last 1 year
WEEKS_IN_FIVE_YEARS = 260   # 260 weeks in the last 5 years


class Stock():
    '''
    A stock is a share in the ownership of a company, with the ticker symbol.
    Methods includes: historical price time series and latest quote.
    '''
    def __init__(self, symbol):
        '''
        This method is the constructor of the stock objects.
        Parameters: symbol -- string, the identifier of the stock ticker
        Return: None
        '''
        self.symbol = symbol

    def interval(self, investor_type):
        '''
        This method returns the interval based on inverstor type.
        Parameters: inverstor_type -- string, based on user input in page
        Return: string, interval
        '''
        if investor_type == "fundamental trader":
            return "monthly"
        if investor_type == "average trader":
            return "weekly"
        if investor_type == "technical trader":
            return "daily"

    def fetch_time_series(self, interval):
        """
        This method returns the time series closing price of the stock.
        parameters: interval -- string, DAILY, WEEKLY or MONTHLY
        return: dictionary, daily/weekly/monthly closing price series
        """
        # If Daily, fetch the daily time series of price data
        if interval == "daily":
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&outputsize=full&apikey={APIKEY}"
            try:
                response = requests.get(url)
                data = response.json()
            except requests.exceptions.ConnectionError:
                return
            if response.status_code != 200:
                return
            key_interval = "Time Series (Daily)"
            dict_complete = data[key_interval]

            # Create the daily closing price time series dictionary
            dict_closing_price = dict()
            list_interval = list(dict_complete.keys())

            # Access closing price data of 252 trading days (last one year)
            for i in range(0, min(TRADE_DAYS_PER_YEAR, len(list_interval))):
                key = list_interval[i]
                closing_price = float(dict_complete[key]["4. close"])
                dict_closing_price[key] = closing_price
            return dict_closing_price

        # If Weekly, fetch the weekly time series of price data
        elif interval == "weekly":
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={self.symbol}&apikey={APIKEY}"
            try:
                response = requests.get(url)
                data = response.json()
            except requests.exceptions.ConnectionError:
                return
            if response.status_code != 200:
                return
            key_interval = "Weekly Adjusted Time Series"
            dict_complete = data[key_interval]

            # Create the weekly closing price time series dictionary
            dict_closing_price = dict()
            list_interval = list(dict_complete.keys())

            # Access closing price data of 260 weeks (last five years)
            for i in range(0, min(WEEKS_IN_FIVE_YEARS, len(list_interval))):
                key = list_interval[i]
                closing_price = float(dict_complete[key]["5. adjusted close"])
                dict_closing_price[key] = closing_price
            return dict_closing_price

        # If Monthly, fetch the monthly time series of price data
        elif interval == "monthly":
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={self.symbol}&apikey={APIKEY}"
            try:
                response = requests.get(url)
                data = response.json()
            except requests.exceptions.ConnectionError:
                return
            if response.status_code != 200:
                return
            key_interval = "Monthly Adjusted Time Series"
            dict_complete = data[key_interval]

            # Create the monthyly closing price time series dictionary
            dict_closing_price = dict()
            list_interval = list(dict_complete.keys())

            # Access all historical data of closing price data
            for key in list_interval:
                closing_price = float(dict_complete[key]["5. adjusted close"])
                dict_closing_price[key] = closing_price
            return dict_closing_price

    def fetch_latest_quote(self):
        """
        This method fetches a latest quote of the stock.
        parameters: None
        return: dictionary, price quote of the stock
        """
        # Fetch the latest quote of the price data of the stock
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.symbol}&apikey={APIKEY}"
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.ConnectionError:
            return
        if response.status_code != 200:
            return
        dict_quote = data["Global Quote"]
        return dict_quote

    def fetch_company_name(self):
        """
        This method fetches the company name of the stock.
        parameters: None
        return: string, company name
        """
        # Fetch the company overview
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey={APIKEY}'
        try:
            response = requests.get(url)
            dict_overview = response.json()
        except requests.exceptions.ConnectionError:
            return
        if response.status_code != 200:
            return
        company_name = dict_overview["Name"]
        return company_name
