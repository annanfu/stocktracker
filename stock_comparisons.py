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
from models.search import Search, SP100
from models.analysis import Analysis
from models.stock import Stock
from helpers import display_header

# Display headers
display_header()
st.header("Stock Comparisons")

try:
    # Display the slider bar of interval choices
    interval = st.select_slider(
        '**Choose the interval you like (daily, weekly, monthly):**',
        options=['daily', 'weekly', 'monthly'],
    )
    st.write(" ")

    # Get user input of no more than 5 stocks
    selections = st.multiselect(
        '**Choose your favourite SP100 stocks for comparison:**',
        SP100,
        placeholder="Hot searches: META, AAPL, AMZN, GOOGL, MSFT")
    if len(selections) > 5:
        raise ValueError

    # Fetch time series and create the price dictionary of the chosen stocks
    dictionary_price_series_of_stock = dict()
    date_list_shortest = []
    for symbol in selections:
        stock = Stock(symbol)
        data = stock.fetch_time_series(interval)
        list_price_series_of_stock = list(data.values())
        dictionary_price_series_of_stock[symbol] = list_price_series_of_stock
        date_list = list(data.keys())
        if date_list_shortest == [] or len(date_list) < len(date_list_shortest):
            date_list_shortest = date_list

    # Create the dictioinary of price series of the chosen stocks
    dictionary_price_series_of_stock_adjust = dict()
    for symbol in dictionary_price_series_of_stock:
        dictionary_price_series_of_stock_adjust[symbol] = dictionary_price_series_of_stock[symbol][0:len(date_list_shortest)]

    # Display the multi-stock price chart of the chosen stocks
    df_price = pd.DataFrame(dictionary_price_series_of_stock_adjust, columns=selections, index=pd.Index((date_list_shortest), name="date"))
    melted_df_price = df_price.reset_index().melt("date", var_name="stock", value_name="price")

    if selections:
        # Create the base line chart
        lines = alt.Chart(melted_df_price).mark_line().encode(
            x='date:T',
            y=alt.Y('price:Q', scale=alt.Scale(zero=False)),
            color='stock',
        )
        # Define the hover state
        hover = alt.selection_single(
                fields=["date"],
                nearest=True,
                on="mouseover",
                empty="none",
        )
        # Create a layer of visual effect upon hover
        layer = alt.layer(
            # Base line chart
            lines,

            # Add a rule mark as a guide line
            alt.Chart().mark_rule(color='#d6d6d6').encode(
                x='date:T'
            ).transform_filter(hover),

            # Add circle marks for selected time points
            lines.mark_circle().encode(
                opacity=alt.condition(hover, alt.value(1), alt.value(0))
            ).add_selection(hover),

            # Add white stroked text to provide a readable background for labels
            lines.mark_text(align='left', dx=5, dy=-5, stroke='white', strokeWidth=2).encode(
                text='price:Q'
            ).transform_filter(hover),

            # Add text labels for stock prices
            lines.mark_text(align='left', dx=5, dy=-5).encode(
                text='price:Q'
            ).transform_filter(hover),
            data=melted_df_price
        )
        chart = (lines + layer).interactive()
        st.altair_chart(chart, use_container_width=True)

    # Create the dictioinary of key financial overview of the chosen stocks
    dictionary_overview_of_stock = dict()
    for symbol in selections:
        analysis = Analysis(symbol)
        data = analysis.company_overview()[0]
        list_values = list(data.values())
        dictionary_overview_of_stock[symbol] = list_values
    list_items = data.keys()
    df = pd.DataFrame(data=dictionary_overview_of_stock, columns=selections, index=pd.Index((list_items), name="Items"))

    # Display the comparison table with the selected items
    index_display = ["LatestQuarter", "PERatio", "OperatingMarginTTM", "EPS", "ReturnOnAssetsTTM", "ReturnOnEquityTTM"]
    st.dataframe(df.loc[index_display], use_container_width=True)

    # Display the notes of definition of each selected item, Source: https://www.investopedia.com/terms/
    st.write("**Note:**")
    st.write("- P/E ratios are used by investors and analysts to determine the relative value of a company's shares in an apples-to-apples comparison to others in the same sector.")
    st.write("- The operating margin represents how efficiently a company is able to generate profit through its core operations.")
    st.write("- Earnings per share (EPS) indicates how much money a company makes for each share of its stock and is a widely used metric for estimating corporate value.")
    st.write("- Return on assets (ROA) is a metric that indicates a company's profitability in relation to its total assets.")
    st.write("- Return on equity (ROE) is a gauge of a corporation's profitability and how efficiently it generates those profits.")
    st.write("- For more details please refer to the source: https://www.investopedia.com/terms/")

except ValueError:
    st.write("You can only choose no more than 5 stocks!")
except NameError:
    st.write("Pick your stocks!")

try:
    # Display the sp100 list at bottom for reference in multiselection
    st.write(" ")
    st.divider()
    st.markdown("- **SP100 component symbol for reference**")
    search = Search()
    sp_100_list = search.display_sp_100_list()
    st.text("\n".join(sp_100_list))
except KeyError:
    st.write("Oops, page overload, please go Home and try again.")
