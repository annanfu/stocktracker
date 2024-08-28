'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
import streamlit as st
from models.investor import Investor
from helpers import display_header, display_link

# Display headers
display_header()
st.header("Get started")

# Display the survey in form, each answer of the questions has a score
st.write("Let's see what type of investor you are:")
question_1_dict = {"Invest conservatively and be willing to bear a certain range of income fluctuations.": 0,
                   "Seeks higher returns and growth of funds and is willing to bear limited losses.": 1,
                   "Hopes to earn high returns and is willing to bear larger losses. ": 2}
question_2_dict = {"Short-term(daily)": 2,
                   "Mid-term(months to half year)": 1,
                   "Long-term(over half year to years)": 0}
question_3_dict = {"Less than 5%": 0, "5% to 25%": 1, "25% to 50%": 2, "More than 50%": 3}

with st.form("my_form"):
    question_1 = st.radio(
        "**Which of the following descriptions best describes your investment attitude?**",
        question_1_dict.keys(),
        index=None,
    )
    question_2 = st.radio(
        "**What is your planned investment period?**",
        question_2_dict.keys(),
        index=None,
    )
    question_3 = st.radio(
        "**What is the maximum investment loss you think you can afford?**",
        question_3_dict.keys(),
        index=None,
    )
    submitted = st.form_submit_button("Submit")

try:
    # Determine the total score and type based on answers, and display the type and descriptions
    score = question_1_dict[question_1] + question_2_dict[question_2] + question_3_dict[question_3]
    investor = Investor()
    investor.determine_type(score)
    st.write(f"You are: **{investor}**")

    # If submitted, pass the type variable to other stock overview page
    if submitted:
        st.write(investor.message())
        display_link(f"/stock_overview/?investor={investor.type}", "Next step: Go to pick your stock")

except NameError:
    st.write("Let me know more about you! Please make your choices. ")
except KeyError:
    st.write("Please answer all the questions before sumbit.")
