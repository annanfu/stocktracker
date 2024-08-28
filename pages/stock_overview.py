'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import streamlit as st
import altair as alt
import pandas as pd
from streamlit_searchbox import st_searchbox
from models.stock import Stock
from models.analysis import Analysis
from models.search import Search
from helpers import display_header, display_link

# SMA periods
PERIOD_TEN_DAY = 10
PERIOD_TWENTY_DAY = 20
PERIOD_SIXTY_DAY = 60
# RSI alert signal thresholds
RSI_UPPER_BOUND = 70
RSI_LOWER_BOUND = 30

# Display headers
display_header()
st.header("Stock Overview")

try:
    # Get the investor passed from the URL
    query_params = st.experimental_get_query_params()
    investor_type = query_params['investor'][0]
    st.write(f"This is a tailored stock overview based on your result of survey as **{investor_type}** type. If the configuration doesn't fit you, please redo the survey or go back home for market overview.")
    display_link("/investor_page", "Redo the survey")
    st.divider()
except NameError:
    st.write("This is an investor-tailored page. Click here to Get started and submit survey first.")
    display_link("/investor_page", "Get started")
    st.stop()
except KeyError:
    st.write("This is an investor-tailored page. Click here to Get started and submit survey first.")
    display_link("/investor_page", "Get started")
    st.stop()

try:
    # Get user's input of stock by keyword
    search = Search()
    symbol = st_searchbox(
        search.search,
        label="⬇️ Enter a company you like ⬇️",
        placeholder="Search: microsoft",
        clear_on_submit=True
    )
    # Create the stock object and get the company name
    stock = Stock(symbol)
    company_name = stock.fetch_company_name()

    # Display the latest quote of the stock and display in three columns
    quote = stock.fetch_latest_quote()
    if quote != {}:
        st.markdown(f"- ### **{company_name} Overview**")
    high_price = quote["03. high"]
    low_price = quote["04. low"]
    closing_price = quote["05. price"]
    last_trading_date = quote["07. latest trading day"]
    previous_price = quote["08. previous close"]
    st.write(f"Last trading day: {last_trading_date}")
    change = quote["10. change percent"]
    col1, col2, col3 = st.columns(3)
    col1.metric("Closing", closing_price, change)
    col2.metric("High", high_price)
    col3.metric("Low", low_price)

    # Display the time series chart of the stock base on interval(investor type)
    stock_interval = stock.interval(investor_type)
    data = stock.fetch_time_series(stock_interval)
    x = list(data.keys())
    y = list(data.values())
    if stock_interval == "daily":
        df = pd.DataFrame({'Last 1 year(Daily time series)': x, 'Price': y})
        chart = alt.Chart(df).mark_line().encode(
            x='Last 1 year(Daily time series)',
            y=alt.Y('Price:Q', scale=alt.Scale(zero=False))
        ).interactive()
    elif stock_interval == "weekly":
        df = pd.DataFrame({'Last 5 years(Weekly time series)': x, 'Price': y})
        chart = alt.Chart(df).mark_line().encode(
            x='Last 5 years(Weekly time series):T',
            y=alt.Y('Price:Q', scale=alt.Scale(zero=False))
        ).interactive()
    elif stock_interval == "monthly":
        df = pd.DataFrame({'Since IPO(Monthly time series)': x, 'Price': y})
        chart = alt.Chart(df).mark_line().encode(
            x='Since IPO(Monthly time series):T',
            y=alt.Y('Price:Q', scale=alt.Scale(zero=False))
        ).interactive()
    st.altair_chart(chart, use_container_width=True)

    # Create an object of Analysis
    analysis = Analysis(symbol)

    # If not fundamental trader, display the technical indicators
    if investor_type != "fundamental trader":
        st.markdown(f"- ### **Technical Indicator Sentiment of {company_name}:**")
        st.write(f"The latest data as of {last_trading_date}")
        tab1, tab2 = st.tabs(["RSI", "SMA"])

        with tab1:
            # Fetch technical indicators RSI
            st.markdown(f"- **RSI(Relative Strength Index) of {company_name}**")
            rsi_value = analysis.rsi_analysis(stock_interval)
            st.metric("RSI", rsi_value)

            # Display the warning signal if reaching threshold
            if float(rsi_value) >= RSI_UPPER_BOUND:
                st.warning(f"⚠️ Alert! 📈RSI reached Overbought Level, RSI that dips below 70 is a bearish signal!")
            elif float(rsi_value) <= RSI_LOWER_BOUND:
                st.warning(f"⚠️ Alert! 📉RSI reached Oversold Level, RSI that moves above 30 is a bullish signal!")
            else:
                st.write("**RSI are in normal range between 30 and 70, there's no obvious trend signal.**")

            # Note source: https://www.investopedia.com/terms/
            st.write("Note: The relative strength index is a momentum indicator that looks at the pace of recent price changes to determine whether a stock is ripe for a rally or a selloff. Market statisticians and traders use the RSI with other technical indicators to identify opportunities to enter or exit a position. When the RSI surpasses the horizontal 30 reference level, it is a bullish sign and when it slides below the horizontal 70 reference level, it is a bearish sign")
            st.write("For more details please refer to the source: https://www.investopedia.com/terms/r/rsi.asp")

        with tab2:
            # Fetch technical indicators SMA
            st.markdown(f"- **SMA(Simple Moving Average) of {company_name}**")
            sma_10_days = analysis.sma_analysis(stock_interval, PERIOD_TEN_DAY)
            sma_20_days = analysis.sma_analysis(stock_interval, PERIOD_TWENTY_DAY)
            sma_60_days = analysis.sma_analysis(stock_interval, PERIOD_SIXTY_DAY)
            col4, col5, col6 = st.columns(3)
            col4.metric("SMA 10 days", sma_10_days)
            col5.metric("SMA 20 days", sma_20_days)
            col6.metric("SMA 60 days", sma_60_days)

            # Display the warning signal if reaching threshold
            if float(sma_10_days) > float(sma_20_days) and float(sma_20_days) > float(sma_60_days):
                st.warning("⚠️ Alert! 📈SMA10 > SMA20 > SMA60, the stock is currently in a LONG position(bullish signal)!")
            elif float(sma_10_days) < float(sma_20_days) and float(sma_20_days) < float(sma_60_days):
                st.warning("⚠️ Alert! 📉SMA10 < SMA20 < SMA60, the stock is currently in a SHORT position(bearish signal)!")
            else:
                st.write("**SMA are in normal range, there's no obvious trend signal.**")

            # Note source: https://www.investopedia.com/terms/
            st.write("Note: Simple Moving Average (SMA) is a technical indicator that is commonly used in financial analysis and trading. Moving averages are versatile tools that can be used to identify trends, support and resistance levels, and other trading opportunities. Simple moving averages can be used in Trend Identification, Support and Resistance, Buy and Sell Signals and Momentum Indicator")
            st.write("For more details please refer to the source: https://www.alphavantage.co/simple_moving_average_sma/")

    # If not technical trader, display the fundamental indicators
    if investor_type != "technical trader":
        st.markdown(f"- ### **Fundamental Indicator of {company_name}:**")
        dict_overview, cut_off_date = analysis.company_overview()
        st.write(f"The latest data as of {cut_off_date}")
        tab1, tab2 = st.tabs(["Company Overview", "Company Value(PE)"])
        with tab1:
            # Fetch fundamental indicators financial data
            st.markdown(f"- **Key financial indicators of {company_name}:**")
            a = list(dict_overview.keys())
            b = list(dict_overview.values())
            df = pd.DataFrame({'Item': a, 'Value': b})
            st.dataframe(df.set_index(df.columns[0]), use_container_width=True)

        with tab2:
            # Calculate the company value PE
            st.markdown(f"- **PE(Price-to-Earnings Ratio) of {company_name}:**")
            price = closing_price
            eps = dict_overview["EPS"]
            pe = round(float(price) / float(eps), 2)
            st.metric("PE", pe)

            # Note source: https://www.investopedia.com/terms/
            st.write("Note: The price-to-earnings (P/E) ratio relates a company's share price to its earnings per share. A high P/E ratio could mean that a company's stock is overvalued, or that investors are expecting high growth rates in the future. Companies that have no earnings or that are losing money do not have a P/E ratio because there is nothing to put in the denominator. A P/E ratio holds the most value to an analyst when compared against similar companies in the same industry or for a single company across a period of time.")
            st.write("For more details please refer to the source: https://www.investopedia.com/terms/p/price-earningsratio.asp")
    st.divider()

    # Fetch related news and display the numbers
    st.markdown(f"- ### **Latest News of {company_name}:**")
    feed = analysis.fetch_news()
    bearish_count, bullish_count = analysis.news_technical_analysis(feed)
    st.write(f"📈Bullish news number: {bullish_count}")
    st.write(f"📉Bearish news number: {bearish_count}")

    # Display the warning signal of bearish news
    if bearish_count != 0:
        st.warning(f"⚠️ Alert! 📉You have {bearish_count} bearish signals in news!")

    # Display the link redirecting to the news page for detials
    if bullish_count != 0 or bearish_count != 0:
        display_link(f"/news/?symbol={symbol}&company={company_name}&investor={investor_type}", "Go to see the news details")

except KeyError:
    st.write("Please search and select a current listed company.")
