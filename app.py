'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on inverstor type.
'''
import streamlit as st
from helpers import display_header, display_link
from st_pages import Page, show_pages, Section

# Display the page header
display_header()

# Rename sidebar page names
show_pages(
    [
        Page("app.py", "Home"),
        Section(name="Investor-tailored Stock Overview"),
        Page("pages/investor_page.py", "investor_page", "▶"),
        Page("pages/stock_overview.py", "stock_overview", "▶"),
        Page("pages/news.py", "news", "▶"),
        Section(name="Custom Stocks Comparison"),
        Page("pages/stock_comparisons.py", "stock_comparisons", "▶"),
    ]
)

# Display the introduction
st.write("Stock Tracker offers a user-friendly interface for tracking stock performance in the US market. See tailored overview based on investor types, or customizable overview for stock comparisons.")

# Display the two main options in home page
col1, col2 = st.columns(2)

with col1:
    st.header("Investor-tailored Stock Overview")
    st.write("Tailored overview and analyses to fit your type.\nFirst, we need to know about you!")
    display_link("/investor_page", "Go")

with col2:
    st.header("Custom Stocks Comparison")
    st.write("Market overview, just casually pick your favourites in S&P100 and see how they performed!")
    display_link("/stock_comparisons", "Go")
