'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import requests
from datetime import date, timedelta

APIKEY = 'DFYILHJL9BDQIV0S'


class Analysis():
    """
    An Analysis is a data analysis based on type with methods of:
    news and sentiment, fundamental indicators, and technical indicators.
    """
    def __init__(self, symbol):
        """
        This method is the constructor of the analysis objects.
        Parameters: symbol -- string, the identifier of the stock ticker
        Return: None
        """
        self.symbol = symbol

    def fetch_news(self):
        """
        This method fetches the news dictionary and out put the list.
        Parameters: None
        Return: list, news feed list
        """
        # Determine the latest system date
        today = date.today()

        # Determine the date of the last day in API format
        one_day_from_today = today - timedelta(days=1)
        one_day_from_today_string = one_day_from_today.isoformat().replace("-", "")
        news_cutoff = one_day_from_today_string + "T0000"

        # Fetch the news dicionary of the stock
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.symbol}&time_from={news_cutoff}&apikey={APIKEY}"
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.ConnectionError:
            return
        if response.status_code != 200:
            return

        # Return the list of news feeds
        list_news_feed = data["feed"]
        return list_news_feed

    def news_technical_analysis(self, list_news_feed):
        """
        This method counts the bullish and bearish news numbers.
        Parameters: list_news_feed -- list of news and sentiment based on user input in page
        Return: tuple of integer, the numbers of bullish and bearish news
        """
        # Initialize the count of news
        bullish_count = 0
        bearish_count = 0

        # Iterate through the list to count the news based on sentiment label
        for news in list_news_feed:
            for ticker in news["ticker_sentiment"]:
                if ticker["ticker"] == self.symbol:
                    if ticker["ticker_sentiment_label"] == "Bearish" or \
                            ticker["ticker_sentiment_label"] == "Somewhat-Bearish":
                        bearish_count += 1
                    elif ticker["ticker_sentiment_label"] == "Bullish" or \
                            ticker["ticker_sentiment_label"] == "Somewhat-Bullish":
                        bullish_count += 1

        # Return tuple of integer, the numbers of bullish and bearish news
        return bearish_count, bullish_count

    def rsi_analysis(self, interval):
        """
        This method returns the latest Relative Strength Index based on the
        interval to determine the data source of daily or weekly.
        Parameters: interval -- string, interval based on investor type
        Return: string, the rsi value in string
        """
        # Fetch time series of rsi based on interval
        url = f"https://www.alphavantage.co/query?function=RSI&symbol={self.symbol}&interval={interval}&time_period=10&series_type=close&apikey={APIKEY}"

        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.ConnectionError:
            return
        if response.status_code != 200:
            return

        # Access the latest date and rsi value in string of the date
        date = data["Meta Data"]["3: Last Refreshed"]
        rsi_value = data["Technical Analysis: RSI"][date]["RSI"]
        return rsi_value

    def sma_analysis(self, interval, period):
        """
        This method returns the Simple Moving Average price based on the
        interval to determine the data source of daily or weekly.
        Parameters: interval -- string, interval based on investor type
                    period -- integer, time period 10/20/60
        Return: string, the sma value of the given period
        """
        # Fetch time series of sma based on interval and period
        url = f"https://www.alphavantage.co/query?function=SMA&symbol={self.symbol}&interval={interval}&time_period={period}&series_type=close&apikey={APIKEY}"

        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.ConnectionError:
            return
        if response.status_code != 200:
            return

        # Access the latest date and sma values in string of the date
        date = data["Meta Data"]["3: Last Refreshed"]
        sma_value = data["Technical Analysis: SMA"][date]["SMA"]

        # Return tuple of strings, the value of the smas
        return sma_value

    def company_overview(self):
        """
        This method returns the company financial data overview.
        Parameters: None
        Return: tuple of dictionary(the financial data dict) and string(cutoff date)
        """
        # Fetch the the company financial data overview
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey={APIKEY}'
        try:
            response = requests.get(url)
            dict_overview = response.json()
        except requests.exceptions.ConnectionError:
            return
        if response.status_code != 200:
            return
        cut_off_date = dict_overview["LatestQuarter"]

        # Return the latest cutoff quarter end and the financial data dict
        return dict_overview, cut_off_date
