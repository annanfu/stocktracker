'''
Annan Fu
CS 5001, Fall 2023
Final Project -- Stock tracker
This application is a stock tracker with tailored features
based on investor type.
'''


class Investor():
    '''
    An investor is a trader with the ownership of stock, with methods of:
    determining the investor type, discription and explanation of the type.
    '''
    def __init__(self):
        '''
        This method is the constructor of the investor objects.
        Parameters: None
        Return: None
        '''
        self.type = ""

    def determine_type(self, score):
        '''
        This method returns the investor type based on score.
        Parameters: score -- integer, total scores based on investor survey
        Return: None
        '''
        if score <= 1:
            self.type = "fundamental trader"
        if score >= 2 and score <= 5:
            self.type = "average trader"
        if score >= 6:
            self.type = "technical trader"

    def __str__(self):
        '''
        This method returns the investor discription based on type.
        Parameters: None
        Return: string, discription of each investor type
        '''
        if self.type == "fundamental trader":
            return ":shield: a Cautious Guardian(fundamental trader)"
        if self.type == "average trader":
            return ":male-office-worker: a Steady Navigator(average trader)"
        if self.type == "technical trader":
            return ":rocket: a Adventurous Explorer(technical trader)"

    def message(self):
        '''
        This method returns the detailed explanation based on type.
        Parameters: None
        Return: string, detailed explanation of each investor type
        '''
        if self.type == "fundamental trader":
            return "As an investor who prioritizes risk aversion, you align with the principles of value investing. Your focus lies in understanding the intrinsic value of stocks, and your investment decisions are primarily informed by **fundamental analysis**. Technical indicators and short-term price fluctuations are of little concern to you. Your evaluation of stock performance focus on **long-term** metrics, often measured on a **monthly** basis, with a keen emphasis on fundamental indicators such as **PE ratio and ROE**."
        if self.type == "average trader":
            return "As a general investor with a balanced risk profile, you may be a beginner in the investment landscape. Consequently, your approach to stock analysis encompasses a comprehensive set of indicators, considering both **fundamental and technical** aspects. Your interest in stock performance is oriented towards the **mid-term**, typically assessed on a **weekly** basis. This approach reflects a holistic view, acknowledging the importance of both fundamental metrics and technical analysis in shaping investment decisions."
        if self.type == "technical trader":
            return "If you identify as a risk-seeking trend trader and speculator, your attention is drawn to stock prices. Decision-making in this realm leans heavily on **technical analysis**, where the focus is on analyzing market sentiment to identify gaming opportunities. Unlike the value investor, you pay little attention to a stock's fundamental attributes or intrinsic value. Your interest in stock performance focus on **short-term** metrics, often assessed on a **daily** basis. Key technical indicators such as **KDJ, RSI, and MA** take precedence in your evaluation process."
