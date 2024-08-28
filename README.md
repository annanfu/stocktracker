## Project Summary

Stock Tracker is an application built on Streamlit framework, offering a user-friendly interface for tracking stock performance in the US market. It assists investors in decision-making by tracking and monitoring the stock data from various dimensions. It provides both tailored overview based on investor types, and customizable market overview for stock comparisons, enhancing the stock tracking experience for investors of different needs.

## How to Run
To run the application, please use the following command in your terminal:
```
pip install streamlit
streamlit run app.py
```

## Description of the REST API(s)

This application use Stock API from Alpha Vantage API as data source by requesting data from the specific url in json format. 

### REST API: Alpha Vantage API

**URL:** https://www.alphavantage.co/

**Documentation:** https://www.alphavantage.co/documentation/

**Description:** I will fetch stock data from Alpha Vantage API in the following four categories: Core Time Series Stock Data APIs, Alpha Intelligence™(News & Sentiment), Fundamental Data, and Technical Indicators.

#### Endpoints:

* `/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={apikey}` - fetch a dictionary of the chosen ticker's daily data time series
* `/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticker}&apikey={apikey}` - fetch a dictionary of the chosen ticker's weekly data time series
* `/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ticker}&apikey={apikey}` - fetch a dictionary of the chosen ticker's monthly data time series
* `/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={APIKEY}` - fetch a dictionary of the chosen ticker's latest quote data
* `/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={APIKEY}` - fetch a dictionary of the chosen ticker's news and sentiment
* `/query?function=RSI&symbol={ticker}}&interval={interval}&time_period={time_period}&series_type=close&apikey={APIKEY}` - fetch a dictionary of the close RSI data of daily/weekly interval in provided day period.
* `/query?function=SMA&symbol={ticker}}&interval={interval}&time_period={time_period}&series_type=close&apikey={APIKEY}` - fetch a dictionary of the close SMA data of daily/weekly interval in provided day period.
* `/query?function=OVERVIEW&symbol={ticker}&apikey={APIKEY}` - fetch a dictionary of the company's fundamental financial data.
* `/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={APIKEY}` - fetch a dictionary of best-match stock information based on the input keyword. 


## List of Features

### Feature 1: Determine investor type

**Description:** By submitting a survey of three questions, the investor type is determined - fundamental, technical, or average trader, which is used to tailor the stock overview page features display. There is no API data in this feature.

**Model (data class):** `Investor`

**REST API endpoint:** None

**Pages:** `investor_page`

### Feature 2: Search box by keyword

**Description:** The search box allows the user to search for the stock symbol by keywords and the dropdown will display the best-match suggestions for the user to select the stock. This endpoint is also used in listing the SP100 component symbol-company reference in the stock comparison page.

**Model (data class):** `Search`

**REST API endpoint:** 
* `/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={APIKEY}`

**Pages:** `stock_overview`,`stock_overview`

### Feature 3: Stock Quote and Time Series Chart

**Description:** Based on the investor type, the application is redirected to the next step - stock overview page. The page gets user input of the stock symbol and displays the latest quote. The historical time series chart is tailored based on different investor types: Technical trader - by daily(252 trading days); Average trader - weekly(260 weeks); Fundamental trader - monthly(since IPO). The chart also support multiple(<= 5) stock comparison (weekly data) in the stock comparison page with customizable interval choice(daily, weekly, monthly).

**Model (data class):** `Stock`

**REST API endpoint:** 
* `/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={apikey}`
* `/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticker}&apikey={apikey}`
* `/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ticker}&apikey={apikey}`
* `/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={APIKEY}`

**Pages:** `stock_overview`, `stock_comparisons`

### Feature 4: Stock Technical Analysis

**Description:** Based on the investor type, if the type is technical/average trader, then the overview will offer technical indicator analysis including RSI(10 days) and SMA(10/20/60 days), and show alerts when there are bullish or bearish signals by reaching the specified threshold. 

**Model (data class):** `Analysis`

**REST API endpoint:** 
* `/query?function=RSI&symbol={ticker}}&interval={interval}&time_period={time_period}&series_type=close&apikey={APIKEY}`
* `/query?function=SMA&symbol={ticker}}&interval={interval}&time_period={time_period}&series_type=close&apikey={APIKEY}` 

**Pages:** `stock_overview`

### Feature 5: Stock Fundamental Analysis

**Description:** Based on the investor type, if the type is fundamental/average trader, then the overview will offer fundamental indicator analysis including key financial indicators and current company value(PE).

**Model (data class):** `Analysis`

**REST API endpoint:** 
* `/query?function=OVERVIEW&symbol={ticker}&apikey={APIKEY}`

**Pages:** `stock_overview`, `stock_comparisons`

### Feature 6: Stock News and Sentiment

**Description:** The overview will offer stock's latest news feed(excluding the neutral ones), show bullish and bearish news numbers, and show alerts with bearish news. There is a link redirecting to the news details in news page.

**Model (data class):** `Analysis`

**REST API endpoint:** 
* `/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={APIKEY}`

**Pages:** `stock_overview`, `news`


## References

**Library - Vega-Altair:** https://altair-viz.github.io/

**Library - Pandas:** https://pandas.pydata.org/docs/

**Library - Streamlit-Searchbox:** https://github.com/m-wrzr/streamlit-searchbox#installation

**Library - Streamlit-St-Pages:** https://github.com/blackary/st_pages

**Text Citation - MA notes:** https://www.alphavantage.co/simple_moving_average_sma/

**Text Citation - Other financial terms notes:** https://www.investopedia.com/terms

**Visualization - Altair Interaction:** https://uwdata.github.io/visualization-curriculum/altair_interaction.html


## Next Steps

### Improve the precision of the current features
Currently, my features of stock overview and analysis reply on criteria and threshold, which are simple and rough. To make the output more reliable and the signal more precise, I plan to improve the precisions of the criteria and threshold if any, including:
* Enrich the survey questions to make the scoring and the invester type more accurate.
* Improve the criteria of technical indicators:
    * SMA: Adding the time series chart, "Support & Resistance" and "Crossovers".
    * RSI: Adding more period for reference, like 20 and 60 day period.
* Improve the criteria of fundamental indicators:
    * PE: Adding more reliable parameter like trailing EPS to determine a more accurate PE.
* Adjust the criteria of news sentiment signal:
    * Sentiment Label: differenciate the "Somewhat Bullish/Bearish" and "Bullish/Bearish".

### Extend the features of the stock analysis
Currently, my features of stock overview and analysis include limited funtionalities with simple signals for investors. To help investors improve their decision-making, I plan to add more features to make the analysis more informative and straightforward:
* Add more technical indicators and determine the overall BUY/SELL signal:
    * By adding more indicators like KDJ, MACD, etc, determine the overall signal based on a comprehensive weighted average bullish/bearish sentiment of each technical indicator.
* Make overview fundamental indicators concise and add more company value dimensions:
    * Exclude the overview index that are less relevant to decision-making, such as shares outstanding.
    * Add PS, PB for for reference in company value, in addtion to PE, if possible, find sources for industry average value so that the comparison would be more meaningful.

### Enrich the customization funtionalities
Currently, the configuration of the tailored stock overview page and the stock comparison page is set by default based on the developer's setting (average consensus). To improve user experience, I plan to make the following adjustments:
* The page should allow the user to customize the interface and show/hide the indicators and analysis according to their needs.
* Add a favourite stock list feature for users to better keep tracking of the stocks.

### Optimize the visualization of the interface
Currently, the interface of each page is simple and plain. I plan to optimize the visulization by introducing some third party components to make the interface, texts and charts more professional and readable.
