'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import streamlit as st
from models.analysis import Analysis
from helpers import display_header, display_link

# Display headers
display_header()
st.header("News")

try:
    # Get the variables(symbol, investor type)from other pages
    query_params = st.experimental_get_query_params()
    symbol = query_params['symbol'][0]
    company_name = query_params['company'][0]
    investor_type = query_params['investor'][0]

    # Display the link redirecting back to the stock overview
    display_link(f"/stock_overview?investor={investor_type}", "View another stock")
    st.markdown(f"- ### **Latest news of {company_name}** ")
    analysis = Analysis(symbol)
    feed = analysis.fetch_news()

    # Display the news details of the chosen stocks(except the neutral ones)
    for news in feed:
        for ticker in news["ticker_sentiment"]:
            if ticker["ticker"] == symbol and ticker["ticker_sentiment_label"] != "Neutral":
                st.markdown(news["title"])
                st.write(news["url"])
                st.write(f"time published: {news['time_published']}")
                st.write(news["summary"])
                st.write(f"news sentiment: {ticker['ticker_sentiment_label']}")
                st.divider()

except KeyError:
    st.write("This is an investor-tailored page. Click here to Get started and submit survey first.")
    display_link("/investor_page/", "Get started")
