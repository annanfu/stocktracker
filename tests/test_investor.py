'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''
from models.investor import Investor


def test_investor_init():
    investor = Investor()
    assert investor.type == ""


def test_investor_determine_type():
    score = 5
    investor = Investor()
    investor.determine_type(score)
    assert investor.type == "average trader"


def test_investor_str():
    investor = Investor()
    investor.type = "average trader"
    assert str(investor) == ":male-office-worker: a Steady Navigator(average trader)"


def test_investor_message():
    investor = Investor()
    investor.type = "fundamental trader"
    assert investor.message() == "As an investor who prioritizes risk aversion, you align with the principles of value investing. Your focus lies in understanding the intrinsic value of stocks, and your investment decisions are primarily informed by **fundamental analysis**. Technical indicators and short-term price fluctuations are of little concern to you. Your evaluation of stock performance focus on **long-term** metrics, often measured on a **monthly** basis, with a keen emphasis on fundamental indicators such as **PE ratio and ROE**."
