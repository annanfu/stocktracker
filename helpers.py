'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on inverstor type.
'''
import streamlit as st


def display_header():
    '''
    This function displays the header and home link.
    Parameters: None
    Return: None
    '''
    # Display header and collapse the sidebar in default
    st.set_page_config(page_title="Stock Tracker", page_icon=":chart_with_upwards_trend:", initial_sidebar_state="collapsed")
    st.title(":blue[Stock Tracker]")
    display_link('/', 'Home')


def display_link(url, text):
    '''
    This function display a link with discription
    Parameters: url -- string, the redirecting link
                text -- string, the discription of the link
    Return: None
    '''
    # Simplify the link function and styling
    st.markdown(f"<a style='font-weight:bold;font-size:18px;text-decoration:none' href='{url}' target='_self'>{text} ▶</a>", unsafe_allow_html=True)
