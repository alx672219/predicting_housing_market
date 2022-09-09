"""CSC110 COVID-19 Final Project: Modelling the Canadian Housing Market

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Terence Liu, Woojin Jang, and Charlie Tao.
"""
import graph as g
import calculations as calc
import datetime
from mortgage import Mortgage
import sys


def run_interrogation() -> dict:
    """Returns a dictionary mapping the question to the answer based on the questions in prompt()
    after interrogating the user.
    """
    # Introduction
    print('Welcome to our interactive model of the Canadian Housing Market. '
          '\nHere you will be able to input your interest %, amount of time, and mortgage to'
          '\ncalculate how much you will be paying compared to the current housing market over the'
          'select amount of time. \n'
          'This calculator does not account for property taxes or insurance, and is only accurate'
          'for mortgages that will be taken in the year 2022 due to the impacts of COVID-19'
          '\n[Press enter to continue]')
    input()
    print('Enter STOP at any time to exit the program.')

    # Recording user input
    final_input = {0: '', 1: '', 2: '', 3: '', 4: '', 5: ''}
    q = 0

    while q < len(final_input):
        prompt(q)
        user_input = input()

        # If stop is initiated, close the loop
        if check_stop(user_input):
            sys.exit()

        # If the input is not a valid answer, ask again
        elif not is_valid_input(user_input, q):
            q -= 1
            print("Please enter a valid value.")

        # Record the user input if it passes all the previous checks.
        else:
            final_input[q] = user_input.lower().strip()

            # If interest rate is variable, no need to ask for the interest rate.
            if q == 0 and final_input[0] == 'variable':
                q += 1
        q += 1

    return final_input


def prompt(selection: int) -> None:
    """Guides the user through the system, with questions in order according to the index in prompts
    """
    prompts = [
        'Is the % interest rate Fixed or Variable?',
        'What is the % interest rate? ex: 3.0 for 3% interest',
        'What is the current property price? ex: 350000 for $350,000',
        'How much mortgage loan is being taken? ex: 350000 for $350,000',
        'How many years is this mortgage set to be paid off by? ex: 15 for 15 years',
        'REMINDER: This program is only accurate towards mortgages that will be taken in 2022'
        '\nWhat month will this mortgage begin? ex: 8 for August'
    ]
    print(prompts[selection])


def is_valid_input(user_in: str, question: int) -> bool:
    """Checks whether the user_input answers the prompt from prompt() properly.

    >>> is_valid_input('', 0)
    False
    """
    clean_input = user_in.lower().strip()

    if question == 0:
        if clean_input in ['fixed', 'variable']:
            return True
    elif question == 1:
        if clean_input.replace('.', '').isnumeric():
            return True
    elif question in [2, 3, 4]:
        if clean_input.isnumeric():
            return True
    elif question == 5:
        if clean_input.isnumeric():
            if int(clean_input) <= 12:
                return True
    return False


def check_stop(user_in: str) -> bool:
    """Checks if the user input is stop
    """
    stop_cues = {'stop'}
    if user_in.lower().strip() in stop_cues:
        return True
    return False


if __name__ == '__main__':
    # Cleaning the user input
    data_lines = {}
    user_answers = run_interrogation()
    date = datetime.date(2022, int(user_answers[5]), 1)

    # Graphing the user's mortgage

    if user_answers[0] == 'variable':
        user_house = Mortgage(user_answers[0], 0.0, float(user_answers[2]), float(user_answers[3]),
                              int(user_answers[4]), date)
        monthly_pay = calc.var_monthly_payment(user_house.principal, calc.proj_rates(1, date),
                                               user_house.period, 1, calc.add_months(date, 1))
        monthly_pay[calc.add_months(date, 13)] = monthly_pay[calc.add_months(date, 1)]
        data_lines['Your Monthly Payment'] = monthly_pay

    else:
        user_house = Mortgage(user_answers[0], float(user_answers[1]), float(user_answers[2]), float(user_answers[3]),
                              int(user_answers[4]), date)
        monthly_pay = calc.fixed_monthly_payment(user_house.principal, user_house.fixed_rate,
                                                 user_house.period, calc.add_months(date, 1))
        monthly_pay[calc.add_months(date, 13)] = monthly_pay[calc.add_months(date, 1)]
        data_lines['Your Monthly Payment'] = monthly_pay

    # Graphing the future potential mortgage
    future_house_monthly = calc.projected_house_price(user_house, 1, False)
    data_lines['Predicted Monthly Payment'] = future_house_monthly

    # Showing the graph
    print('Press Enter when you are ready to load the graph.')
    input()
    g.graph_data(data_lines)
    sys.exit()
